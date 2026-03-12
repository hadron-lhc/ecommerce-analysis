import streamlit as st
import sqlite3
from pathlib import Path
import pandas as pd
import sys
from streamlit_extras.add_vertical_space import add_vertical_space


sys.path.insert(0, str(Path(__file__).parent.parent))

from app.components.sidebar import sidebar


def estrucutura_web():
    st.set_page_config(layout="wide")
    st.title("E-commerce Dashboard")
    add_vertical_space(5)
    st.subheader("Sales, customer, and product analysis.")

    add_vertical_space(2)

    add_vertical_space(3)
    # metricas, total de clientes, total de productos y total de ordenes
    st.divider()
    conn = st.session_state.conn
    total_clients = pd.read_sql_query("SELECT COUNT(*) FROM clients", conn).iloc[0, 0]
    total_products = pd.read_sql_query("SELECT COUNT(*) FROM products", conn).iloc[0, 0]
    total_orders = pd.read_sql_query("SELECT COUNT(*) FROM orders", conn).iloc[0, 0]
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Clients", total_clients)
    col2.metric("Total Products", total_products)
    col3.metric("Total Orders", total_orders)

    add_vertical_space(7)

    # "Generate your own data and see how the analysis charts change"
    st.markdown(
        "<h3 style='font-size: 24px; color:#ddd; '> - Generate your own data and see how the analysis charts change -</h3>",
        unsafe_allow_html=True,
    )


def main():
    sidebar()
    if "conn" not in st.session_state:
        st.session_state.conn = sqlite3.connect(
            Path(__file__).parent.parent / "database" / "ecommerce.db",
            check_same_thread=False,
        )
    estrucutura_web()


if __name__ == "__main__":
    main()
