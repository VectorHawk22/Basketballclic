import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

class Database:
    def __init__(self):
        # Параметры подключения
        self.params = {
            'host': Config.DB_HOST,
            'port': Config.DB_PORT,
            'database': Config.DB_NAME,
            'user': Config.DB_USER,
            'password': Config.DB_PASSWORD
        }
    
    def get_connection(self):
        """Создаем соединение с БД"""
        return psycopg2.connect(**self.params)
    
    def execute(self, query, params=None):
        """
        Выполняем запрос к БД
        Возвращает: список словарей (результаты) или None
        """
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(query, params or ())
                
                # Если это SELECT - возвращаем результаты
                if cur.description:
                    return cur.fetchall()
                
                # Если INSERT/UPDATE/DELETE - коммитим
                conn.commit()
                return None
        finally:
            conn.close()
    
    def execute_one(self, query, params=None):
        """Выполняет запрос и возвращает одну запись"""
        results = self.execute(query, params)
        return results[0] if results else None

# Создаем глобальный объект для работы с БД
db = Database()