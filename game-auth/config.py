import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Настройки БД
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'user_files_db')
    DB_USER = os.getenv('DB_USER', 'coder')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    
    # Секретный ключ
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')