import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def send_notification(subject, body, to_email):
    """Send an email notification."""
    # Email configuration
    sender_email = os.getenv("SENDER_EMAIL")  # Set your sender email in .env
    sender_password = os.getenv("SENDER_PASSWORD")  # Set your sender email password in .env

    # Create the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach the email body
    msg.attach(MIMEText(body, 'plain'))

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print("Notification sent successfully!")
    except Exception as e:
        print(f"Failed to send notification: {e}")
