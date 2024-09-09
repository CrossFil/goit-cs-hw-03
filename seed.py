from faker import Faker
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

# Створення з'єднання з базою даних
conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    dbname=db_name,
    user=db_user,
    password=db_password
)

cur = conn.cursor()
fake = Faker()

# Додавання випадкових даних для таблиці users
for _ in range(10):
    cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fake.name(), fake.email()))

# Додавання даних для таблиці status
statuses = [('new',), ('in progress',), ('completed',)]
cur.executemany("INSERT INTO status (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;", statuses)

# Додавання випадкових даних для таблиці tasks
for _ in range(20):
    cur.execute(
        "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
        (fake.sentence(), fake.text(), fake.random_int(1, 3), fake.random_int(1, 10))
    )

# Збереження змін
conn.commit()

# Закриття курсора і з'єднання
cur.close()
conn.close()
