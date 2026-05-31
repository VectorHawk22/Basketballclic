CREATE DATABASE IF NOT EXISTS user_files_db;
USE user_files_db;

-- Таблица пользователей
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Таблица файлов пользователей
CREATE TABLE user_files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT DEFAULT 0,
    mime_type VARCHAR(100),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
-- Создание суперпользователя (с полными правами)
CREATE USER 'artman'@'%' IDENTIFIED BY 'strong_password_123';

-- Создание пользователя «игра» (с ограниченными правами)
CREATE USER 'game'@'%' IDENTIFIED BY '1q2w3e4r5t6y';
-- Предоставление всех привилегий суперпользователю
GRANT ALL PRIVILEGES ON user_files_db.* TO 'superuser'@'%';

-- Предоставление привилегий  игре
GRANT SELECT, INSERT, UPDATE, DELETE, EXECUTE ON user_files_db.* TO 'game'@'%';
FLUSH PRIVILEGES;



