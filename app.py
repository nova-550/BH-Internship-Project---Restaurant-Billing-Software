import streamlit as st
import sqlite3

if 'cart' not in st.session_state:
    st.session_state.cart = []  # Holds dicts of item: qty


def fetch_menu():
    conn = sqlite3.connect('db/restaurant.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, category, price, gst FROM menu")
    items = cursor.fetchall()
    conn.close()
    return items

menu_items = fetch_menu()
menu_by_category = {}

def add_to_cart(item_name, qty, price, gst):
    found = False
    for entry in st.session_state.cart:
        if entry['item'] == item_name:
            entry['qty'] = qty
            found = True
            break
    if not found and qty > 0:
        st.session_state.cart.append({'item': item_name, 'qty': qty, 'price': price, 'gst': gst})
    st.session_state.cart.clear()

    add_to_cart(name, qty, price, gst)


# Categorize
for item in menu_items:
    name, category, price, gst = item
    menu_by_category.setdefault(category, []).append(item)

st.subheader("📜 Menu")
for category, items in menu_by_category.items():
    st.markdown(f"### 🍽️ {category}")
    for item in items:
        name, _, price, gst = item
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"**{name}** - ₹{price} (+{gst}% GST)")
        with col2:
            qty = st.number_input(f"Qty_{name}", min_value=0, max_value=10, step=1, key=f"{name}_qty")
            if qty > 0:
                st.session_state.cart.append({'item': name, 'qty': qty, 'price': price, 'gst': gst})

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

        st.write(f"{item} x {qty} = ₹{item_total:.2f} + GST ₹{gst_amount:.2f}")

    grand_total = total + gst_total
    st.success(f"**Total (incl. GST): ₹{grand_total:.2f}**")
else:
    st.info("No items in the cart yet.")

   
# if st.button("Clear Cart"):
#     st.session_state.cart.clear()
#     st.success("Cart cleared!")
# st.markdown("---")
# st.subheader("📦 Checkout")
