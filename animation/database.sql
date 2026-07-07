-- Создание базы данных
CREATE DATABASE user_files_db;

-- Подключение к базе данных (выполняется вне SQL-скрипта, например, в psql: \c user_files_db)

-- Таблица пользователей
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Функция для обновления updated_at при изменении записи
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Таблица категорий файлов
CREATE TABLE file_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица файлов пользователей
CREATE TABLE user_files (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    file_name VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT DEFAULT 0,
    file_hash VARCHAR(64), -- для SHA‑256, предотвращение дубликатов
    mime_type VARCHAR(100),
    category_id INTEGER REFERENCES file_categories(id),
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE
);

-- Связь файлов с категориями (многие‑ко‑многим)
CREATE TABLE user_files_categories (
    file_id INTEGER NOT NULL REFERENCES user_files(id) ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES file_categories(id) ON DELETE CASCADE,
    PRIMARY KEY (file_id, category_id)
);

-- Таблица версий файлов
CREATE TABLE file_versions (
    id SERIAL PRIMARY KEY,
    file_id INTEGER NOT NULL REFERENCES user_files(id) ON DELETE CASCADE,
    version_number INTEGER NOT NULL,
    file_path VARCHAR(500) NOT NULL, -- путь к версии файла
    file_size BIGINT DEFAULT 0,
    change_description TEXT,
    created_by INTEGER NOT NULL REFERENCES users(id), -- кто создал версию
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица логирования действий
CREATE TABLE user_actions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id),
    action_type VARCHAR(50) NOT NULL, -- 'upload', 'delete', 'download', 'update'
    file_id INTEGER REFERENCES user_files(id),
    details JSONB, -- дополнительные данные в JSONB
    ip_address INET, -- тип для IP‑адресов
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание индексов для ускорения запросов
CREATE INDEX idx_user_files_user_id ON user_files(user_id);
CREATE INDEX idx_user_files_uploaded_at ON user_files(uploaded_at);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_user_files_user_date ON user_files(user_id, uploaded_at);
CREATE UNIQUE INDEX idx_user_files_hash ON user_files(file_hash);
CREATE INDEX idx_user_actions_timestamp ON user_actions(timestamp);

-- Добавление базовых категорий
INSERT INTO file_categories (name, description) VALUES
('Saves', 'Игровые сохранения'),
('Configs', 'Конфигурационные файлы'),
('Backups', 'Резервные копии'),
('Others', 'Прочие файлы');

-- Функция загрузки файла (аналог хранимой процедуры)
CREATE OR REPLACE FUNCTION upload_user_file(
    p_user_id INTEGER,
    p_file_name VARCHAR,
    p_file_path VARCHAR,
    p_file_size BIGINT,
    p_mime_type VARCHAR,
    p_description TEXT,
    p_category_id INTEGER
) RETURNS INTEGER AS $$
DECLARE
    new_file_id INTEGER;
BEGIN
    INSERT INTO user_files (user_id, file_name, file_path, file_size, mime_type, description, category_id)
    VALUES (p_user_id, p_file_name, p_file_path, p_file_size, p_mime_type, p_description, p_category_id)
    RETURNING id INTO new_file_id;

    -- Логируем действие
    INSERT INTO user_actions (user_id, action_type, file_id, details)
    VALUES (p_user_id, 'upload', new_file_id,
            jsonb_build_object('file_name', p_file_name));

    RETURN new_file_id;
END;
$$ LANGUAGE plpgsql;

-- Функция получения файлов пользователя
CREATE OR REPLACE FUNCTION get_user_files(p_user_id INTEGER)
RETURNS TABLE(
    file_id INTEGER,
    file_name VARCHAR,
    file_size BIGINT,
    uploaded_at TIMESTAMP,
    category_name VARCHAR,
    version_count INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        uf.id,
        uf.file_name,
        uf.file_size,
        uf.uploaded_at,
        fc.name as category_name,
        (SELECT COUNT(*) FROM file_versions fv WHERE fv.file_id = uf.id) as version_count
    FROM user_files uf
    LEFT JOIN file_categories fc ON uf.category_id = fc.id
    WHERE uf.user_id = p_user_id AND uf.is_active = TRUE
    ORDER BY uf.uploaded_at DESC;
END;
$$ LANGUAGE plpgsql;

-- Триггер на удаление файла
CREATE OR REPLACE FUNCTION log_file_delete()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO user_actions (user_id, action_type, file_id, details)
    VALUES (OLD.user_id, 'delete', OLD.id,
           jsonb_build_object('file_name', OLD.file_name));
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_file_delete
    AFTER DELETE ON user_files
    FOR EACH ROW EXECUTE FUNCTION log_file_delete();

-- Триггер на обновление файла
CREATE OR REPLACE FUNCTION log_file_update()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.file_name != NEW.file_name OR OLD.description != NEW.description THEN
        INSERT INTO user_actions (user_id, action_type, file_id, details)
        VALUES (NEW.user_id, 'update', NEW.id,
               jsonb_build_object(
                   'old_name', OLD.file_name,
                   'new_name', NEW.file_name
               ));
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_file_update
    AFTER UPDATE ON user_files
    FOR EACH ROW EXECUTE FUNCTION log_file_update();

-- Создание ролей и назначение привилегий
CREATE ROLE superuser WITH LOGIN PASSWORD 'your_super_secure_password';
CREATE ROLE game WITH LOGIN PASSWORD 'your_game_secure_password';

GRANT ALL PRIVILEGES ON DATABASE user_files_db TO superuser;
GRANT CONNECT ON DATABASE user_files_db TO game;

-- Даём права на все таблицы и последовательности
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO superuser;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO superuser;

GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO game;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO game;

-- Автоматические права для новых таблиц
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO superuser;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO game;
