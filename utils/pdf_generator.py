from fpdf import FPDF
import os

def generate_pdf_receipt(order_details, total, order_id):
    """Generate PDF receipt with error handling"""
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Add receipt content
        pdf.cell(200, 10, txt=f"Receipt for Order #{order_id}", ln=True)
        
        # Ensure receipts directory exists
        os.makedirs("receipts", exist_ok=True)
        
        # Save the file
        filepath = f"receipts/receipt_{order_id}.pdf"
        pdf.output(filepath)
        return filepath
    except Exception as e:
        raise Exception(f"Failed to generate PDF: {str(e)}")
