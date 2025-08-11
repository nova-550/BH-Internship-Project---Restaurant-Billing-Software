# Restaurant Order Management & Billing System

A simple web application for managing restaurant orders, including order placement, payment processing, and receipt generation.

## Features

- User-friendly interface for placing orders
- Payment processing
- Receipt generation in PDF format
- Order summary and sales reporting
- SQLite database for data storage

## Technologies Used

- Python
- Streamlit
- SQLite
- FPDF (for PDF generation)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/restaurant-order-management.git
   cd restaurant-order-management
   ```

2. **Create a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Mac Windows
   venv\Scripts\activate    # For Windows
   ```

3. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database: Run the following command to set up the SQLite database:**
   ```bash
   python -c "from utils.db_utils import init_db; init_db()"
   ```

## Usage
1. **Run the application:**
   ```bash
   streamlit run main.py
   ```
2. **Access the application:** Open your web browser and go to http://localhost:8501.

3. **Place an order:**

    - Select items from the menu.
    - Enter any customer notes.
    - Click on "Process Payment" to complete the order.

4. **Download Receipt:** After processing the payment, you will have the option to download the receipt in PDF format.

## Contributing
Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.