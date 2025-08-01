import sqlite3

conn = sqlite3.connect("db/restaurant.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())  # Should show [('menu',), ...]

cursor.execute("SELECT * FROM menu;")
print("Rows:", cursor.fetchall())  # Should list your menu items


# name,category,price,gst
# Margherita Pizza,Main Course,250,5
# Paneer Butter Masala,Main Course,200,5
# Butter Naan,Bread,30,5
# Cold Coffee,Beverages,80,5
# Chocolate Brownie,Dessert,90,5
# Veg Burger,Snacks,120,5
# Masala Dosa,South Indian,100,5

