import sqlite3
import os

DB_PATH = os.path.join("db", "restaurant.db")

def get_all_bills():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")  # Assuming your table is named 'orders'
    bills = cursor.fetchall()
    conn.close()
    return bills
