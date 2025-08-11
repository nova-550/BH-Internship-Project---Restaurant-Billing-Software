import os

# Directory for storing receipts
RECEIPT_DIR = "receipts"
   

# Ensure the receipts directory exists
if not os.path.exists(RECEIPT_DIR):
    os.makedirs(RECEIPT_DIR)

# Email configuration (if needed)
ADMIN_EMAIL = "pshivraj935@gmail.com"  # Change to your admin email
# Retrieve the admin password from an environment variable
ADMIN_PASSWORD = "admin"  # Change this!  
