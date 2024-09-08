from pymongo import MongoClient

# Підключення до MongoDB з використанням рядка підключення
client = MongoClient('mongodb+srv://CrossFil:741801d@crossfil.m1vu2.mongodb.net/task2?retryWrites=true&w=majority&appName=CrossFil')

# Вибір бази даних і колекції
db = client["task2"]
collection = db["cats_collection"]

print("Підключення до MongoDB встановлено успішно!")

# Функція для додавання нового запису (Create)
def add_cat(name, age, features):
    try:
        cat = {
            "name": name,
            "age": age,
            "features": features
        }
        result = collection.insert_one(cat)
        print(f"Кіт доданий з _id: {result.inserted_id}")
    except Exception as e:
        print(f"Сталася помилка при додаванні кота: {e}")

# Функція для виведення всіх записів із колекції (Read)
def get_all_cats():
    try:
        cats = collection.find()
        for cat in cats:
            print(cat)
    except Exception as e:
        print(f"Сталася помилка при отриманні котів: {e}")

# Функція для виведення інформації про кота за ім'ям (Read)
def get_cat_by_name(name):
    try:
        cat = collection.find_one({"name": name})
        if cat:
            print(cat)
        else:
            print(f"Кіт з ім'ям {name} не знайдений.")
    except Exception as e:
        print(f"Сталася помилка при отриманні інформації про кота: {e}")

# Функція для оновлення віку кота за ім'ям (Update)
def update_cat_age(name, new_age):
    try:
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.matched_count > 0:
            print(f"Вік кота {name} оновлено до {new_age}.")
        else:
            print(f"Кіт з ім'ям {name} не знайдений.")
    except Exception as e:
        print(f"Сталася помилка при оновленні віку кота: {e}")

# Функція для додавання нової характеристики до списку features кота за ім'ям (Update)
def add_feature_to_cat(name, new_feature):
    try:
        result = collection.update_one({"name": name}, {"$push": {"features": new_feature}})
        if result.matched_count > 0:
            print(f"Характеристика '{new_feature}' додана коту {name}.")
        else:
            print(f"Кіт з ім'ям {name} не знайдений.")
    except Exception as e:
        print(f"Сталася помилка при додаванні характеристики коту: {e}")

# Функція для видалення запису з колекції за ім'ям тварини (Delete)
def delete_cat_by_name(name):
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Кіт з ім'ям {name} видалений.")
        else:
            print(f"Кіт з ім'ям {name} не знайдений.")
    except Exception as e:
        print(f"Сталася помилка при видаленні кота: {e}")

# Функція для видалення всіх записів із колекції (Delete)
def delete_all_cats():
    try:
        result = collection.delete_many({})
        print(f"Всі коти видалені. Кількість видалених записів: {result.deleted_count}.")
    except Exception as e:
        print(f"Сталася помилка при видаленні всіх котів: {e}")

# Тестування функцій
if __name__ == "__main__":
    # Додавання тестових котів
    add_cat("barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])
    add_cat("murzik", 5, ["грається з іграшками", "сіро-білий", "любить молоко"])

    # Читання всіх котів
    print("\nВсі коти в колекції:")
    get_all_cats()

    # Читання кота за ім'ям
    print("\nІнформація про кота 'barsik':")
    get_cat_by_name("barsik")

    # Оновлення віку кота
    print("\nОновлення віку кота 'barsik' до 4 років:")
    update_cat_age("barsik", 4)

    # Додавання нової характеристики
    print("\nДодавання нової характеристики 'любитъ рибу' коту 'murzik':")
    add_feature_to_cat("murzik", "любить рибу")

    # Видалення кота за ім'ям
    print("\nВидалення кота 'barsik':")
    delete_cat_by_name("barsik")

    # Видалення всіх котів
   # print("\nВидалення всіх котів з колекції:")
   # delete_all_cats()
