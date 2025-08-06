from datetime import datetime
import os

def generate_receipt(order_items, total):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    receipt_lines = [
        "🍽️ Restaurant Receipt",
        f"Date & Time: {timestamp}",
        "-" * 40,
        f"{'Item':<20}{'Qty':<5}{'Price':<7}",
        "-" * 40
    ]

    for item in order_items:
        name = item['name']
        qty = item['quantity']
        price = item['price']
        line_total = price * qty
        receipt_lines.append(f"{name:<20}{qty:<5}₹{line_total:.2f}")

    receipt_lines.append("-" * 40)
    receipt_lines.append(f"{'Total':<30}₹{total:.2f}")
    receipt_lines.append("-" * 40)
    receipt_lines.append("Thank you for dining with us! 🙏")

    filename = f"receipt_{now.strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = os.path.join("receipts", filename)
    os.makedirs("receipts", exist_ok=True)

    with open(filepath, "w", encoding='utf-8') as f:
        f.write("\n".join(receipt_lines))

    return filepath
