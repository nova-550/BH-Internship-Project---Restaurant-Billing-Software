import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_sales_report(to_email, subject, body):
    """Send a sales report via email."""
    from_email = "your_email@example.com"  # Replace with your email
    password = "your_password"  # Replace with your email password

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
