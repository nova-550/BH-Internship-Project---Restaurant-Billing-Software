import sqlite3
import os

DB_PATH = os.path.join("db", "restaurant.db")

def clear_order_history():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders")
    conn.commit()
    conn.close()
    print("Order history cleared.")

if __name__ == "__main__":
    clear_order_history()
