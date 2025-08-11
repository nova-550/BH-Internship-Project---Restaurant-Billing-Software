import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join("db", "restaurant.db")

def init_db():
    """Initialize database with proper schema"""
    os.makedirs("db", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Enable WAL mode for better concurrency
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                items TEXT NOT NULL,
                total REAL NOT NULL,
                order_type TEXT,
                customer_notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'completed'
            )
        """)
        conn.commit()
    except Exception as e:
        print(f"Database error: {str(e)}")
    finally:
        conn.close()

def insert_order(order, total, order_type=None, customer_notes=None):
    """Insert order with error handling and verification"""
    os.makedirs("db", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        items_str = "|".join([
            f"{item['id']}:{item['name']}:{item['price']}:{item['quantity']}" 
            for item in order
        ])
        
        cursor.execute(
            """INSERT INTO orders 
            (items, total, order_type, customer_notes) 
            VALUES (?, ?, ?, ?)""",
            (items_str, total, order_type, customer_notes)
        )
        order_id = cursor.lastrowid
        conn.commit()
        
        # Verify insertion
        cursor.execute("SELECT id FROM orders WHERE id = ?", (order_id,))
        if not cursor.fetchone():
            raise Exception("Order verification failed - not found in database")
            
        return order_id
    except Exception as e:
        conn.rollback()
        raise Exception(f"Failed to create order: {str(e)}")
    finally:
        conn.close()


def update_schema():
    """Add status column if missing"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if status column exists
        cursor.execute("PRAGMA table_info(orders)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'status' not in columns:
            print("Adding status column...")
            cursor.execute("ALTER TABLE orders ADD COLUMN status TEXT DEFAULT 'completed'")
            conn.commit()
            print("Schema updated successfully")
        else:
            print("Status column already exists")
            
    except Exception as e:
        print(f"Schema update failed: {e}")
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
    """Get sales summary with backward compatibility"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # First check if status column exists
        cursor.execute("PRAGMA table_info(orders)")
        columns = [col[1] for col in cursor.fetchall()]
        has_status = 'status' in columns
        
        query = """
            SELECT 
                SUM(total) as total_sales, 
                COUNT(*) as total_orders,
                AVG(total) as avg_order
            FROM orders
            """ 
        
        # Only filter by status if the column exists
        if has_status:
            query += " WHERE status = 'completed'"
        
        params = []
        if start_date and end_date:
            query += " AND " if has_status else " WHERE "
            query += "date(created_at) BETWEEN ? AND ?"
            params.extend([start_date, end_date])
        
        cursor.execute(query, params)
        result = cursor.fetchone()
        
        return {
            "total_sales": result[0] or 0,
            "total_orders": result[1] or 0,
            "avg_order": result[2] or 0
        }
    finally:
        conn.close()

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

