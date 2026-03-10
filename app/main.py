import streamlit as st
import sqlite3
from pathlib import Path
import pandas as pd
from streamlit_extras.add_vertical_space import add_vertical_space


def estrucutura_web():
    st.title("E-commerce Dashboard")
    add_vertical_space(3)
    st.subheader("Análisis de ventas, clientes y productos")
    add_vertical_space(5)

    # metricas, total de clientes, total de productos y total de ordenes
    conn = st.session_state.conn
    total_clientes = pd.read_sql_query("SELECT COUNT(*) FROM clients", conn).iloc[0, 0]
    total_productos = pd.read_sql_query("SELECT COUNT(*) FROM products", conn).iloc[
        0, 0
    ]
    total_ordenes = pd.read_sql_query("SELECT COUNT(*) FROM orders", conn).iloc[0, 0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Clientes", total_clientes)
    col2.metric("Total Productos", total_productos)
    col3.metric("Total Ordenes", total_ordenes)


def main():
    if "conn" not in st.session_state:
        st.session_state.conn = sqlite3.connect(
            Path(__file__).parent.parent / "database" / "ecommerce.db"
        )

    estrucutura_web()


if __name__ == "__main__":
    main()
