import sqlite3
import csv
# import pandas as pd
import os

DB_PATH = os.path.join("db", "restaurant.db")

def init_db():
    """Initialize or update the database schema"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # First check if the table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'")
    table_exists = cursor.fetchone()
    
    if table_exists:
        # Check if created_at column exists
        cursor.execute("PRAGMA table_info(orders)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'created_at' not in columns:
            # Step 1: Add the column without a default value
            cursor.execute("ALTER TABLE orders ADD COLUMN created_at DATETIME")
            
            # Step 2: Update existing rows to set created_at to the current timestamp
            cursor.execute("UPDATE orders SET created_at = CURRENT_TIMESTAMP")
            
            # Step 3: Set the default value for future inserts
            cursor.execute("CREATE TABLE new_orders (id INTEGER PRIMARY KEY AUTOINCREMENT, items TEXT NOT NULL, total REAL NOT NULL, order_type TEXT, customer_notes TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP)")
            cursor.execute("INSERT INTO new_orders (id, items, total, order_type, customer_notes, created_at) SELECT id, items, total, order_type, customer_notes, created_at FROM orders")
            cursor.execute("DROP TABLE orders")
            cursor.execute("ALTER TABLE new_orders RENAME TO orders")
            
            conn.commit()
    else:
        # Create new table with all columns
        cursor.execute("""
            CREATE TABLE orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                items TEXT NOT NULL,
                total REAL NOT NULL,
                order_type TEXT,
                customer_notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    
    conn.close()


def insert_order(order, total, order_type=None, customer_notes=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        items_str = "; ".join([f"{item['name']} x {item['quantity']}" for item in order])
        cursor.execute(
            "INSERT INTO orders (items, total, order_type, customer_notes) VALUES (?, ?, ?, ?)",
            (items_str, total, order_type, customer_notes)
        )
        order_id = cursor.lastrowid
        conn.commit()
        return order_id
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()


def get_all_orders(start_date=None, end_date=None):
    """Retrieve all orders from the database within a date range."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = "SELECT * FROM orders"
    params = []
    
    if start_date and end_date:
        query += " WHERE created_at BETWEEN ? AND ?"
        params.extend([start_date, end_date])
    
    cursor.execute(query, params)
    orders = cursor.fetchall()
    
    conn.close()
    return orders


def get_sales_summary(start_date=None, end_date=None):
    """Retrieve a summary of sales from the database within a date range."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = "SELECT SUM(total) FROM orders"
    params = []
    
    if start_date and end_date:
        query += " WHERE created_at BETWEEN ? AND ?"
        params.extend([start_date, end_date])
    
    cursor.execute(query, params)
    total_sales = cursor.fetchone()[0] or 0  # Handle case where there are no orders
    cursor.execute("SELECT COUNT(*) FROM orders" + ("" if not params else " WHERE created_at BETWEEN ? AND ?"), params)
    total_orders = cursor.fetchone()[0] or 0  # Handle case where there are no orders
    
    conn.close()
    return {
        "total_sales": total_sales,
        "total_orders": total_orders
    }


def get_top_items(start_date=None, end_date=None):
    """Retrieve the top-selling items from the database within a date range."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    query = "SELECT items, SUM(total) as total_sales FROM orders"
    params = []
    
    if start_date and end_date:
        query += " WHERE created_at BETWEEN ? AND ?"
        params.extend([start_date, end_date])
    
    query += " GROUP BY items ORDER BY total_sales DESC LIMIT 10"
    
    cursor.execute(query, params)
    top_items = cursor.fetchall()
    
    conn.close()
    return top_items


def clear_test_data():
    """Clear all data from the orders table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM orders")
    conn.commit()
    conn.close()

def export_to_csv(order, file_path):
    """Export all orders to a CSV file."""
    orders = get_all_orders()
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Items", "Total", "Order Type", "Customer Notes", "Created At"])  # Header
        for order in orders:
            writer.writerow(order)

def check_db_integrity():
    """Check the integrity of the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        # Check if the orders table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders';")
        table_exists = cursor.fetchone() is not None
        
        # Check for any integrity constraints
        cursor.execute("PRAGMA integrity_check;")
        integrity_check = cursor.fetchone()[0]
        
        return {
            "table_exists": table_exists,
            "integrity_check": integrity_check
        }
    finally:
        conn.close()
