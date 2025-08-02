import sqlite3

conn = sqlite3.connect("db/restaurant.db")
cursor = conn.cursor()

# Drop and recreate the menu table
cursor.execute("DROP TABLE IF EXISTS menu")
cursor.execute("""
    CREATE TABLE menu (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT,
        price REAL,
        gst REAL
    )
""")

menu_data = [
    ('Paneer Butter Masala', 'Main Course', 240, 5),
    ('Veg Biryani', 'Main Course', 180, 5),
    ('Masala Dosa', 'Breakfast', 80, 5),
    ('Gulab Jamun', 'Dessert', 40, 5),
    ('Chai', 'Beverage', 20, 5)
]

cursor.executemany("INSERT INTO menu (name, category, price, gst) VALUES (?, ?, ?, ?)", menu_data)

# ✅ Add the orders table
cursor.execute("DROP TABLE IF EXISTS orders")
cursor.execute("""
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT,
        item TEXT,
        quantity INTEGER,
        price REAL,
        gst REAL,
        total REAL,
        timestamp TEXT
    )
""")

conn.commit()
conn.close()
