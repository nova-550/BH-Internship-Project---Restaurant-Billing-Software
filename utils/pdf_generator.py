from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_pdf_receipt(order, total, discount):
    receipt_path = os.path.join("receipts", f"receipt_{int(total)}.pdf")
    
    c = canvas.Canvas(receipt_path, pagesize=letter)
    width, height = letter
    
    c.drawString(100, height - 100, "Receipt")
    c.drawString(100, height - 120, "Items:")
    
    y_position = height - 140
    for item in order:
        c.drawString(100, y_position, f"{item['name']} x {item['quantity']} - ₹{item['price'] * item['quantity']:.2f}")
        y_position -= 20
    
    c.drawString(100, y_position, f"Subtotal: ₹{total:.2f}")
    c.drawString(100, y_position - 20, f"Discount: {discount}%")
    c.drawString(100, y_position - 40, f"Total: ₹{total * (1 - discount / 100):.2f}")
    
    c.save()
    return receipt_path
