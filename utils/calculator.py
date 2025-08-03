# File: utils/calculator.py

def calculate_total(order):
    return sum(item['price'] * item['quantity'] for item in order)
