from faker import Faker
import psycopg2

# Створення з'єднання з базою даних
conn = psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="task_1",
        user="postgres",
        password="741801"
    )
#conn = psycopg2.connect("dbname=task_1 user=postgres password=741801")
cur = conn.cursor()
fake = Faker()

# Додавання випадкових даних
for _ in range(10):
    cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fake.name(), fake.email()))

statuses = [('new',), ('in progress',), ('completed',)]
cur.executemany("INSERT INTO status (name) VALUES (%s)", statuses)

for _ in range(20):
    cur.execute(
        "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
        (fake.sentence(), fake.text(), fake.random_int(1, 3), fake.random_int(1, 10))
    )

conn.commit()
cur.close()
conn.close()
