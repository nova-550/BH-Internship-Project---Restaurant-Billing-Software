from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_pdf_receipt(order_items, total_price, order_id):
    # Directory to save PDFs
    output_dir = "receipts"
    os.makedirs(output_dir, exist_ok=True)

    # File path
    filename = f"receipt_{order_id}.pdf"
    file_path = os.path.join(output_dir, filename)

    # Create canvas
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    # Heading
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 50, "Nova Grocery Store 🛒")

    # Subheading
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, height - 75, f"Order Receipt - ID: {order_id}")

    # Timestamp
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.drawCentredString(width / 2, height - 95, f"Date: {now}")

    # Draw line
    c.line(40, height - 105, width - 40, height - 105)

    # List items
    c.setFont("Helvetica", 12)
    y = height - 130
    for item in order_items:
        c.drawString(50, y, f"- {item}")
        y -= 20

    # Total
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, y - 10, f"Total Amount: ₹{total_price:.2f}")

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 40, "Thank you for shopping with us!")
    c.drawString(50, 25, "Visit again 🌟")

    # Save PDF
    c.save()

    return file_path
