import sqlite3

def connect_db():
    return sqlite3.connect("db/restaurant.db")

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS menu (
            item_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            price REAL NOT NULL,
            gst REAL DEFAULT 5.0
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            mode TEXT CHECK(mode IN ('Dine-in', 'Takeaway')),
            payment_method TEXT CHECK(payment_method IN ('Cash', 'Card', 'UPI')),
            subtotal REAL,
            gst_amount REAL,
            discount REAL,
            total REAL,
            timestamp TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            item_id INTEGER,
            order_id INTEGER,
            quantity INTEGER,
            FOREIGN KEY (item_id) REFERENCES menu(item_id),
            FOREIGN KEY (order_id) REFERENCES orders(order_id)
        );
    """)

    conn.commit()
    conn.close()
