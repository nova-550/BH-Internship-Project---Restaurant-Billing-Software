import os

# Directory for storing receipts
RECEIPT_DIR = os.path.join(os.getcwd(), "receipts")

# Ensure the receipts directory exists
if not os.path.exists(RECEIPT_DIR):
    os.makedirs(RECEIPT_DIR)

# Email configuration (if needed)
ADMIN_EMAIL = "admin@example.com"  # Change to your admin email
# Retrieve the admin password from an environment variable
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")  # Use a default if not set
