import streamlit as st
import sqlite3
from datetime import datetime

# Initialize session state
if 'cart' not in st.session_state:
    st.session_state.cart = []  # List of dicts: {item, qty, price, gst}

if 'order_placed' not in st.session_state:
    st.session_state.order_placed = False

def fetch_menu():
    conn = sqlite3.connect("db/restaurant.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category, price, gst FROM menu")
    rows = cursor.fetchall()
    conn.close()
    return rows

menu_items = fetch_menu()
menu_by_category = {}

# Categorize items by category properly and keep item dicts
for item in menu_items:
    item_id, name, category, price, gst = item
    if category not in menu_by_category:
        menu_by_category[category] = []
    menu_by_category[category].append({
        'id': item_id,
        'name': name,
        'price': price,
        'gst': gst
    })

st.title("🍽️ Restaurant Billing System")
st.subheader("📜 Menu")

# Clear cart button for testing/demo
if st.button("🧹 Clear Cart"):
    st.session_state.cart.clear()
    st.session_state.order_placed = False
    # st.query_params = {}  # clears query parameters (optional)
    st.stop()

# Display Menu grouped by category
for category, items in menu_by_category.items():
    st.markdown(f"### 🍴 {category}")
    for item in items:
        item_id = item['id']
        name = item['name']
        price = item['price']
        gst = item['gst']

        col1, col2 = st.columns([4, 2])
        with col1:
            st.markdown(f"**{name}** - ₹{price} (+{gst}% GST)")
        with col2:
            qty = st.number_input(
                f"Qty_{item_id}_{name}",
                min_value=0,
                max_value=10,
                step=1,
                key=f"{item_id}_{name}_qty"
            )

            # Update cart accordingly
            found = False
            for entry in st.session_state.cart:
                if entry['item'] == name:
                    if qty == 0:
                        # Remove item if qty is zero
                        st.session_state.cart.remove(entry)
                    else:
                        # Update qty
                        entry['qty'] = qty
                    found = True
                    break
            if not found and qty > 0:
                st.session_state.cart.append({
                    'item': name,
                    'qty': qty,
                    'price': price,
                    'gst': gst
                })

st.markdown("---")
st.subheader("🛒 Current Order")

if st.session_state.cart:
    total = 0
    gst_total = 0
    for entry in st.session_state.cart:
        item = entry['item']
        qty = entry['qty']
        price = entry['price']
        gst = entry['gst']

        item_total = price * qty
        gst_amount = (item_total * gst) / 100
        total += item_total
        gst_total += gst_amount

        st.write(f"**{item} x {qty}** = ₹{item_total:.2f} + GST ₹{gst_amount:.2f}")

    grand_total = total + gst_total
    st.success(f"**Total (incl. GST): ₹{grand_total:.2f}**")

    customer_name = st.text_input("👤 Enter Customer Name")
    if not customer_name:
        st.warning("Please enter the customer's name to proceed with the order.")

    # Place Order Button
    if st.button("✅ Place Order"):
        st.session_state.order_placed = True

        # Optional DB storage (add later)
        # store_order_to_db(st.session_state.cart, grand_total)

        st.success("🎉 Order placed successfully!")

        # Show Bill Summary
        with st.expander("📄 View Bill Summary"):
            for entry in st.session_state.cart:
                item_total = entry['price'] * entry['qty']
                gst_amt = (item_total * entry['gst']) / 100
                st.write(f"{entry['item']} x {entry['qty']} = ₹{item_total:.2f} + ₹{gst_amt:.2f} GST")

            st.markdown(f"### 🧾 **Grand Total: ₹{grand_total:.2f}**")
            st.markdown(f"🕒 Time: {datetime.now().strftime('%d-%m-%Y %I:%M %p')}")
        # Store order in session state

        if customer_name.strip() == "":
            st.warning("Please enter customer name before placing the order.")
            st.stop()

        conn = sqlite3.connect("db/restaurant.db")
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for entry in st.session_state.cart:
            item_total = entry['price'] * entry['qty']
            gst_amt = (item_total * entry['gst']) / 100
            grand_total = item_total + gst_amt

            cursor.execute('''
                INSERT INTO orders (customer_name, item, quantity, price, gst, total, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                customer_name,
                entry['item'],
            entry['qty'],
            entry['price'],
            entry['gst'],
            grand_total,
            timestamp
        ))

        conn.commit()
        conn.close()

        # Clear cart after order
        st.session_state.cart.clear()

else:
    st.info("🛒 Your cart is empty. Add items to proceed.")

st.markdown("---")
st.subheader("📚 Order History")

conn = sqlite3.connect("db/restaurant.db")
cursor = conn.cursor()

cursor.execute("SELECT customer_name, item, quantity, total, timestamp FROM orders ORDER BY timestamp DESC")
rows = cursor.fetchall()
conn.close()

if rows:
    for row in rows[:10]:  # Show latest 10 orders
        cust_name, item, qty, total, time = row
        st.write(f"🧾 **{cust_name}** ordered **{item} x {qty}** | ₹{total:.2f} on 🕒 {time}")
else:
    st.info("No orders placed yet.")
