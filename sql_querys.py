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

# Функція для підключення до бази даних
def connect():
    return psycopg2.connect(
        host=db_host,
        port=db_port,
        dbname=db_name,
        user=db_user,
        password=db_password
    )

# Функція для виконання SELECT-запитів
def execute_select(query, params=None):
    conn = connect()
    cur = conn.cursor()
    cur.execute(query, params)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

# Функція для виконання INSERT, UPDATE, DELETE-запитів
def execute_query(query, params=None):
    conn = connect()
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    cur.close()
    conn.close()

# Запити

# 1. Отримати всі завдання певного користувача
tasks_for_user_1 = execute_select("SELECT * FROM tasks WHERE user_id = %s;", (1,))
print(tasks_for_user_1)

# 2. Вибрати завдання за певним статусом
tasks_with_status_new = execute_select("""
    SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = %s);
""", ('new',))
print(tasks_with_status_new)

# 3. Оновити статус конкретного завдання.
task_id = 1 # замініть на необхідний id завдання
execute_query("""
    UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = %s) WHERE id = %s;
""", ('in progress', task_id))

# 4. Отримати список користувачів, які не мають жодного завдання
users_without_tasks = execute_select("SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks);")
print(users_without_tasks)

# 5. Додати нове завдання для конкретного користувача. 
user_id = 1 # замініть на необхідний id користувача
execute_query("""
    INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s);
""", ('New Task', 'Task description', 1, user_id))

# 6. Отримати всі завдання, які ще не завершено.
tasks_not_completed = execute_select("""
    SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = %s);
""", ('completed',))
print(tasks_not_completed)

# 7. Видалити конкретне завдання.
task_id_to_delete = 1 # замініть на необхідний id завдання
execute_query("DELETE FROM tasks WHERE id = %s;", (task_id_to_delete,))

# 8. Знайти користувачів з певною електронною поштою. 
users_with_example_email = execute_select("SELECT * FROM users WHERE email LIKE %s;", ('%@example.com',))
print(users_with_example_email)

# 9. Оновити ім'я користувача.
user_id_to_update = 1 # замініть на необхідний id користувача
execute_query("UPDATE users SET fullname = %s WHERE id = %s;", ('New Name', user_id_to_update))

# 10. Отримати кількість завдань для кожного статусу.
status_task_counts = execute_select("""
    SELECT s.name, COUNT(t.id) AS task_count FROM status s LEFT JOIN tasks t ON s.id = t.status_id GROUP BY s.name;
""")
print(status_task_counts)

# 11. Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти. 
tasks_for_users_with_example_email = execute_select("""
    SELECT t.* FROM tasks t JOIN users u ON t.user_id = u.id WHERE u.email LIKE %s;
""", ('%@example.com',))
print(tasks_for_users_with_example_email)

# 12. Отримати список завдань, що не мають опису. 
tasks_with_empty_description = execute_select("SELECT * FROM tasks WHERE description IS NULL OR description = '';")
print(tasks_with_empty_description)

# 13. Вибрати користувачів та їхні завдання, які є у статусі
users_with_in_progress_tasks = execute_select("""
    SELECT u.*, t.* FROM users u INNER JOIN tasks t ON u.id = t.user_id 
    WHERE t.status_id = (SELECT id FROM status WHERE name = %s);
""", ('in progress',))
print(users_with_in_progress_tasks)

# 14. Отримати користувачів та кількість їхніх завдань.
user_task_counts = execute_select("""
    SELECT u.fullname, COUNT(t.id) AS task_count FROM users u 
    LEFT JOIN tasks t ON u.id = t.user_id GROUP BY u.fullname;
""")
print(user_task_counts)
