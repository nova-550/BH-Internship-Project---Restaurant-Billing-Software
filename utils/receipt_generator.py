# utils/receipt_generator.py

from datetime import datetime
import os

def generate_receipt(order_items, total, gst_total, restaurant_name="BroskiesHub Café"):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    receipt_lines = [
        f"{restaurant_name}",
        f"Date & Time: {timestamp}",
        "-" * 40,
        f"{'Item':<20}{'Qty':<5}{'Price':<7}{'GST%':<5}",
        "-" * 40
    ]

    for item in order_items:
        name = item['item']
        qty = item['qty']
        price = item['price']
        gst = item['gst']
        receipt_lines.append(f"{name:<20}{qty:<5}{price:<7}{gst:<5}")

    receipt_lines.append("-" * 40)
    receipt_lines.append(f"{'Subtotal':<30}₹{total:.2f}")
    receipt_lines.append(f"{'GST Total':<30}₹{gst_total:.2f}")
    receipt_lines.append(f"{'Grand Total':<30}₹{total + gst_total:.2f}")
    receipt_lines.append("-" * 40)
    receipt_lines.append("Thank you for dining with us! 🙏")

    receipt_text = "\n".join(receipt_lines)
    filename = f"receipt_{now.strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = os.path.join("receipts", filename)
    os.makedirs("receipts", exist_ok=True)

    with open(filepath, "w", encoding='utf-8') as f:
        f.write(receipt_text)

    return filepath


# import os
# from datetime import datetime

# def generate_receipt(order_items, total_amount, payment_method):
#     now = datetime.now()
#     timestamp = now.strftime("%Y%m%d_%H%M%S")
#     receipt_name = f"receipt_{timestamp}.txt"
#     receipt_dir = os.path.join(os.getcwd(), "receipts")
#     os.makedirs(receipt_dir, exist_ok=True)
#     receipt_path = os.path.join(receipt_dir, receipt_name)

#     with open(receipt_path, "w") as f:
#         f.write("==== RESTAURANT RECEIPT ====\n")
#         f.write(f"Date: {now.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
#         f.write("Items:\n")
#         for item in order_items:
#             f.write(f"{item['name']} x {item['qty']} = ₹{item['total']}\n")
#         f.write("\n")
#         f.write(f"Total Amount: ₹{total_amount}\n")
#         f.write(f"Payment Method: {payment_method}\n")
#         f.write("============================\n")

#     return receipt_path
