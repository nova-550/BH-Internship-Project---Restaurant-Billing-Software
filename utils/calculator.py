def calculate_total(order):
    """Calculate the total price of the order."""
    return sum(item['price'] * item['quantity'] for item in order)

def apply_discount(total, discount_percentage):
    """Apply a discount to the total price."""
    if discount_percentage < 0 or discount_percentage > 100:
        raise ValueError("Discount percentage must be between 0 and 100.")
    discount_amount = (discount_percentage / 100) * total
    return total - discount_amount
