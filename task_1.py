import psycopg2
from dotenv import load_dotenv
import os

# Завантаження змінних середовища з файлу .env
load_dotenv()

# Отримання конфігураційних даних з .env
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

# Підключення до бази даних
conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    dbname=db_name,
    user=db_user,
    password=db_password
)

# Створення курсора для виконання SQL-запитів
cur = conn.cursor()

# SQL-запити для створення таблиць
create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);
"""

create_status_table = """
CREATE TABLE IF NOT EXISTS status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);
"""

create_tasks_table = """
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status_id INTEGER REFERENCES status(id),
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
);
"""

# Виконання запитів для створення таблиць
try:
    cur.execute(create_users_table)
    cur.execute(create_status_table)
    cur.execute(create_tasks_table)
    print("Таблиці успішно створені.")
except Exception as e:
    print(f"Помилка при створенні таблиць: {e}")

# Вставка початкових даних у таблицю статусів
insert_statuses = """
INSERT INTO status (name) VALUES 
('new'),
('in progress'),
('completed')
ON CONFLICT (name) DO NOTHING;
"""

try:
    cur.execute(insert_statuses)
    print("Дані про статуси успішно вставлені.")
except Exception as e:
    print(f"Помилка при вставці даних: {e}")

# Закриття курсора і збереження змін
cur.close()
conn.commit()

# Закриття підключення
conn.close()
