import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_sales_report(to_email, subject, body):
    """Send a sales report via email."""
    from_email = os.getenv("EMAIL_USER")  # Use environment variable for email
    password = os.getenv("EMAIL_PASSWORD")  # Use environment variable for password

    # Ensure body is a string
    if not isinstance(body, str):
        body = str(body)  # Convert to string if not already

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Set up the server
        server = smtplib.SMTP('smtp.gmail.com', 587)  # Use your email provider's SMTP server
        server.starttls()  # Upgrade the connection to a secure encrypted SSL/TLS connection
        server.login(from_email, password)  # Log in to your email account
        server.send_message(msg)  # Send the email
        server.quit()  # Close the server connection
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Example usage
if __name__ == "__main__":
    to_email = "recipient@example.com"  # Replace with recipient's email
    subject = "Sales Report"
    body = "This is the body of the sales report."  # Replace with actual report content
    send_sales_report(to_email, subject, body)
