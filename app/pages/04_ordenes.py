import pandas as pd
import sqlite3
from pathlib import Path
import streamlit as st
import sys

from streamlit_extras.add_vertical_space import add_vertical_space

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.generate_data import generar_ordenes
from src.clean import limpiar_ordenes
from app.components.sidebar import sidebar

DATABASE_PATH = Path(__file__).parent.parent.parent / "database" / "ecommerce.db"


def obtener_ordenes(conn):
    query = """
        SELECT
            c.name as cliente,
            p.name as producto,
            p.category as categoria,
            o.unitary_price precio_unitario,
            o.mount as cantidad,
            o.total,
            o.order_date as fecha_orden,
            o.state as estado
        FROM orders o
        JOIN clients c ON c.id = o.client_id
        JOIN products p ON p.id_product = o.product_id
    """
    df_ordenes = pd.read_sql_query(query, conn)
    df_ordenes["fecha_orden"] = pd.to_datetime(
        df_ordenes["fecha_orden"], format="mixed"
    )
    return df_ordenes


def main():
    sidebar()
    st.markdown("<h1 style='text-align: center;'>Orders</h1>", unsafe_allow_html=True)
    add_vertical_space(3)

    st.set_page_config(layout="wide")
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)

    df_ordenes = obtener_ordenes(conn)
    df_ordenes["fecha_orden"] = pd.to_datetime(df_ordenes["fecha_orden"])

    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        status = ["All"] + df_ordenes["estado"].unique().tolist()
        status_selected = st.selectbox("Filter by status", status)

    with col2:
        start_date = df_ordenes["fecha_orden"].min().date()
        end_date = df_ordenes["fecha_orden"].max().date()

        date_range = st.date_input(
            "Date range: ", value=(start_date, end_date), key="date_filter"
        )

        if isinstance(date_range, tuple) and len(date_range) == 2:
            inicio = pd.Timestamp(date_range[0])
            fin = pd.Timestamp(date_range[1])
        elif isinstance(date_range, tuple) and len(date_range) == 1:
            inicio = pd.Timestamp(date_range[0])
            fin = pd.Timestamp(df_ordenes["fecha_orden"].max())
        else:
            inicio = pd.Timestamp(df_ordenes["fecha_orden"].min())
            fin = pd.Timestamp(df_ordenes["fecha_orden"].max())

        df_filtered = df_ordenes[df_ordenes["fecha_orden"].between(inicio, fin)]

    if status_selected != "All":
        df_filtered = df_filtered[df_filtered["estado"] == status_selected]

    df_filtered = df_filtered.copy()
    df_filtered["fecha_orden"] = df_filtered["fecha_orden"].dt.date

    st.dataframe(df_filtered)

    st.divider()
    st.subheader("Add orders")

    df_clients = pd.read_sql_query("SELECT * FROM clients", conn)
    df_products = pd.read_sql_query("SELECT * FROM products", conn)

    tab1, tab2, tab3 = st.tabs(["Generate Random", "Add Manually", "Delete"])

    with tab1:
        n = st.number_input(
            "Number of orders to generate", min_value=1, max_value=50, value=1
        )
        if st.button("Generate orders"):
            df_nuevos = generar_ordenes(df_products, df_clients, n)
            df_nuevos_limpios = limpiar_ordenes(df_nuevos)
            df_nuevos_limpios.to_sql("orders", conn, if_exists="append", index=False)
            st.success(f"✅ {n} orders generated successfully")

    with tab2:
        with st.form("Add order"):
            cliente = st.selectbox(
                "Client", sorted(df_clients["name"].unique().tolist())
            )

            producto = st.selectbox(
                "Product", sorted(df_products["name"].unique().tolist())
            )

            cantidad = st.number_input("Quantity", min_value=1, value=1)

            estado = st.selectbox(
                "Status", sorted(df_ordenes["estado"].unique().tolist())
            )

            submitted = st.form_submit_button("Save order")

            if submitted:
                conn.execute(
                    """
                    INSERT INTO orders (client_id, product_id, unitary_price, mount, total, order_date, state)
                    VALUES (
                        (SELECT id FROM clients WHERE name = ?),
                        (SELECT id_product FROM products WHERE name = ?),
                        (SELECT price FROM products WHERE name = ?),
                        ?,
                        (SELECT price FROM products WHERE name = ?) * ?,
                        DATE('now'),
                        ?
                    )
                """,
                    (cliente, producto, producto, cantidad, producto, cantidad, estado),
                )
                conn.commit()
                st.success("✅ Order added successfully")

    with tab3:
        n_borrar = st.number_input(
            "Number of orders to delete",
            min_value=1,
            max_value=50,
            value=1,
        )
        if st.button("Delete orders"):
            conn.execute(
                """
                DELETE FROM orders
                WHERE order_id IN (
                    SELECT order_id
                    FROM orders
                    WHERE order_id IS NOT NULL
                    ORDER BY order_date DESC
                    LIMIT ?
                )
            """,
                (n_borrar,),
            )
            conn.commit()
            st.success(f"✅ {n_borrar} orders deleted successfully")


if __name__ == "__main__":
    main()
