import sqlite3
import os

DB_PATH = os.path.join("db", "restaurant.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            items TEXT NOT NULL,
            total REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def fetch_menu_items():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price FROM menu")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "name": row[1], "price": row[2]} for row in rows]

def insert_order(order, total):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    items_str = "; ".join([f"{item['name']} x {item['quantity']}" for item in order])
    cursor.execute("INSERT INTO orders (items, total) VALUES (?, ?)", (items_str, total))
    conn.commit()
    conn.close()
