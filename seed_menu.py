import sqlite3
import os

DB_PATH = os.path.join("db", "restaurant.db")

MENU = [
    ("Paneer Butter Masala", 180),
    ("Chicken Biryani", 220),
    ("Butter Naan", 40),
    ("Veg Pulao", 150),
    ("Cold Drink", 30),
]

def seed_menu():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS menu (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, price REAL NOT NULL)")
    cursor.executemany("INSERT INTO menu (name, price) VALUES (?, ?)", MENU)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    seed_menu()
    print("Menu seeded successfully.")
else:
    print("Menu seeding module imported. Call seed_menu() to seed the database.")