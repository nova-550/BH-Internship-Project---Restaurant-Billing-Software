from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_pdf_receipt(order_items, total_price):
    output_dir = "receipts"
    os.makedirs(output_dir, exist_ok=True)

    filename = f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    file_path = os.path.join(output_dir, filename)

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 50, "Restaurant Receipt")

    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 75, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    c.setFont("Helvetica", 12)
    y = height - 100
    for item in order_items:
        c.drawString(50, y, f"{item['name']} x {item['quantity']} - ₹{item['price'] * item['quantity']:.2f}")
        y -= 20

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y - 10, f"Total Amount: ₹{total_price:.2f}")

    c.save()
    return file_path
