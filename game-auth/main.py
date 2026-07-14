from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from passlib.context import CryptContext
import jwt
import datetime
from database import db
from config import Config

# ============================================
# 1. НАСТРОЙКА ПРИЛОЖЕНИЯ
# ============================================

app = FastAPI(title="Game Auth Server")

# Разрешаем запросы с любых адресов (для игры)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Настройка хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ============================================
# 2. МОДЕЛИ ДАННЫХ (что приходит в запросе)
# ============================================

class RegisterRequest(BaseModel):
    """Модель для регистрации"""
    username: str
    password: str
    confirm_password: str

class LoginRequest(BaseModel):
    """Модель для входа"""
    username: str
    password: str

class ChangePasswordRequest(BaseModel):
    """Модель для смены пароля"""
    old_password: str
    new_password: str
    confirm_password: str

# ============================================
# 3. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================

def hash_password(password: str) -> str:
    """Хэшируем пароль (делаем его нечитаемым)"""
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    """Проверяем, правильный ли пароль"""
    return pwd_context.verify(password, hashed)

def create_token(user_id: int, username: str) -> str:
    """
    Создаем JWT-токен (как электронный пропуск)
    Токен действует 7 дней
    """
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }
    return jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')

def decode_token(token: str):
    """Расшифровываем токен и получаем данные пользователя"""
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return payload
    except:
        return None

def get_current_user(token: str):
    """
    Проверяем токен и возвращаем пользователя
    Эта функция используется для защиты эндпоинтов
    """
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Недействительный токен")
    
    # Проверяем, существует ли пользователь
    user = db.execute_one(
        "SELECT id, username, is_active FROM users WHERE id = %s",
        (payload['user_id'],)
    )
    
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    
    if not user['is_active']:
        raise HTTPException(status_code=403, detail="Аккаунт заблокирован")
    
    return user

# ============================================
# 4. API ЭНДПОИНТЫ (то, что будет вызывать игра)
# ============================================

@app.post("/api/register")
def register(data: RegisterRequest):
    """
    РЕГИСТРАЦИЯ НОВОГО ИГРОКА
    """
    # Шаг 1: Проверяем, совпадают ли пароли
    if data.password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Пароли не совпадают")
    
    # Шаг 2: Проверяем длину пароля
    if len(data.password) < 6:
        raise HTTPException(status_code=400, detail="Пароль должен быть минимум 6 символов")
    
    # Шаг 3: Проверяем, не занято ли имя
    existing = db.execute_one(
        "SELECT id FROM users WHERE username = %s",
        (data.username,)
    )
    if existing:
        raise HTTPException(status_code=409, detail="Имя пользователя уже занято")
    
    # Шаг 4: Хэшируем пароль
    hashed_password = hash_password(data.password)
    
    # Шаг 5: Создаем пользователя в БД
    user = db.execute_one(
        """
        INSERT INTO users (username, password_hash, is_active)
        VALUES (%s, %s, true)
        RETURNING id, username, is_active, created_at
        """,
        (data.username, hashed_password)
    )
    
    # Шаг 6: Логируем действие
    db.execute(
        """
        INSERT INTO user_actions (user_id, action_type, details)
        VALUES (%s, %s, %s)
        """,
        (user['id'], 'register', f'{{"username": "{data.username}"}}')
    )
    
    # Шаг 7: Создаем токен
    token = create_token(user['id'], user['username'])
    
    # Шаг 8: Отправляем ответ
    return {
        "success": True,
        "message": "Регистрация успешна!",
        "data": {
            "user": {
                "id": user['id'],
                "username": user['username'],
                "is_active": user['is_active']
            },
            "token": token
        }
    }

@app.post("/api/login")
def login(data: LoginRequest):
    """
    ВХОД В ИГРУ
    """
    # Шаг 1: Ищем пользователя в БД
    user = db.execute_one(
        "SELECT id, username, password_hash, is_active FROM users WHERE username = %s",
        (data.username,)
    )
    
    # Шаг 2: Если пользователь не найден
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    # Шаг 3: Проверяем, активен ли аккаунт
    if not user['is_active']:
        raise HTTPException(status_code=403, detail="Аккаунт заблокирован")
    
    # Шаг 4: Проверяем пароль
    if not verify_password(data.password, user['password_hash']):
        # Логируем неудачную попытку
        db.execute(
            """
            INSERT INTO user_actions (user_id, action_type, details)
            VALUES (%s, %s, %s)
            """,
            (None, 'failed_login', f'{{"username": "{data.username}"}}')
        )
        raise HTTPException(status_code=401, detail="Неверный пароль")
    
    # Шаг 5: Логируем успешный вход
    db.execute(
        """
        INSERT INTO user_actions (user_id, action_type, details)
        VALUES (%s, %s, %s)
        """,
        (user['id'], 'login', f'{{"username": "{data.username}"}}')
    )
    
    # Шаг 6: Обновляем время последнего входа
    db.execute(
        "UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = %s",
        (user['id'],)
    )
    
    # Шаг 7: Создаем токен
    token = create_token(user['id'], user['username'])
    
    # Шаг 8: Отправляем ответ
    return {
        "success": True,
        "message": "Вход выполнен!",
        "data": {
            "user": {
                "id": user['id'],
                "username": user['username'],
                "is_active": user['is_active']
            },
            "token": token
        }
    }

@app.get("/api/profile")
def profile(token: str):
    """
    ПОЛУЧЕНИЕ ПРОФИЛЯ (требуется токен)
    """
    user = get_current_user(token)
    
    return {
        "success": True,
        "data": {
            "id": user['id'],
            "username": user['username'],
            "is_active": user['is_active']
        }
    }

@app.post("/api/change-password")
def change_password(data: ChangePasswordRequest, token: str):
    """
    СМЕНА ПАРЛЯ (требуется токен)
    """
    # Шаг 1: Проверяем токен и получаем пользователя
    user = get_current_user(token)
    
    # Шаг 2: Проверяем новый пароль
    if data.new_password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Пароли не совпадают")
    
    if len(data.new_password) < 6:
        raise HTTPException(status_code=400, detail="Пароль должен быть минимум 6 символов")
    
    # Шаг 3: Получаем текущий хэш пароля
    current = db.execute_one(
        "SELECT password_hash FROM users WHERE id = %s",
        (user['id'],)
    )
    
    # Шаг 4: Проверяем старый пароль
    if not verify_password(data.old_password, current['password_hash']):
        raise HTTPException(status_code=401, detail="Неверный старый пароль")
    
    # Шаг 5: Обновляем пароль
    new_hash = hash_password(data.new_password)
    db.execute(
        "UPDATE users SET password_hash = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s",
        (new_hash, user['id'])
    )
    
    # Шаг 6: Логируем
    db.execute(
        """
        INSERT INTO user_actions (user_id, action_type, details)
        VALUES (%s, %s, %s)
        """,
        (user['id'], 'change_password', '{"success": true}')
    )
    
    return {
        "success": True,
        "message": "Пароль успешно изменен"
    }

@app.post("/api/logout")
def logout(token: str):
    """
    ВЫХОД ИЗ ИГРЫ (логируем, токен не отзываем)
    """
    user = get_current_user(token)
    
    db.execute(
        """
        INSERT INTO user_actions (user_id, action_type, details)
        VALUES (%s, %s, %s)
        """,
        (user['id'], 'logout', '{"success": true}')
    )
    
    return {
        "success": True,
        "message": "Выход выполнен"
    }

@app.get("/health")
def health():
    """Проверка, что сервер работает"""
    return {"status": "alive"}

# ============================================
# 5. ЗАПУСК СЕРВЕРА
# ============================================

if __name__ == "__main__":
    import uvicorn
    print("🚀 Сервер запускается...")
    print("📝 Документация: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)