# # reset_db.py

# from utils.db_utils import create_tables
# from data.seed_menu import seed_menu  # You can make this a callable function

# create_tables()
# seed_menu()
# print("✅ Database reset with default menu.")

import sqlite3
import os

DB_PATH = os.path.join("db", "restaurant.db")

def clear_order_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables:", tables)

    if ('orders',) in tables:
        cursor.execute("DELETE FROM orders")
        conn.commit()
        print("Order history cleared.")
    else:
        print("❌ 'orders' table not found in database.")

    conn.close()

if __name__ == "__main__":
    clear_order_history()
