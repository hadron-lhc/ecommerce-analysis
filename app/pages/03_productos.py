import pandas as pd
import sqlite3
from pathlib import Path
import streamlit as st
import sys

from streamlit_extras.add_vertical_space import add_vertical_space

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.generate_data import generar_productos
from src.clean import limpiar_productos
from app.components.sidebar import sidebar

DATABASE_PATH = Path(__file__).parent.parent.parent / "database" / "ecommerce.db"


def obtener_productos(conn):
    query = """
        SELECT
            name,
            category,
            price,
            stock
        FROM
            products
    """

    df = pd.read_sql_query(query, conn)
    return df


def main():
    sidebar()
    st.markdown(
        "<h1 style='text-align: center;'>Products</h1>", unsafe_allow_html=True
    )
    add_vertical_space(3)

    st.set_page_config(layout="wide")
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)

    df_products = obtener_productos(conn)

    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        category = ["All"] + sorted(df_products["category"].unique().tolist())
        category_selected = st.selectbox("Filter by category", category)

    with col2:
        min_price = 0
        max_price = int(df_products["price"].max())

        price_range = st.select_slider(
            "Select price range:",
            options=range(min_price, max_price + 1),
            value=(min_price, max_price),
        )

        df_filtered = df_products[
            (df_products["price"] >= price_range[0])
            & (df_products["price"] <= price_range[1])
        ]

    if category_selected != "All":
        df_filtered = df_filtered[df_filtered["category"] == category_selected]

    st.dataframe(df_filtered)

    st.divider()
    st.subheader("Add products")

    tab1, tab2, tab3 = st.tabs(["Generate Random", "Add Manually", "Delete"])

    with tab1:
        n = st.number_input(
            "Number of products to generate", min_value=1, max_value=50, value=1
        )
        if st.button("Generate products"):
            df_nuevos = generar_productos(n)
            df_nuevos_limpios = limpiar_productos(df_nuevos)
            df_nuevos_limpios.to_sql("products", conn, if_exists="append", index=False)
            st.success(f"✅ {n} products generated successfully")

    with tab2:
        with st.form("form_product"):
            nombre = st.text_input("Name")
            categoria = st.selectbox(
                "Category", sorted(df_products["category"].unique().tolist())
            )
            precio = st.number_input("Price")

            submitted = st.form_submit_button("Save product")

            if submitted:
                conn.execute(
                    """
                    INSERT INTO products (category, name, price)
                    VALUES (?, ?, ?)
                """,
                    (categoria, nombre, precio),
                )
                conn.commit()
                st.success(f"✅ Product {nombre} added successfully")
    with tab3:
        n_borrar = st.number_input(
            "Number of products to delete",
            min_value=1,
            max_value=50,
            value=1,
        )
        if st.button("Delete products"):
            conn.execute(
                f"DELETE FROM products WHERE id_product IN (SELECT id_product FROM products ORDER BY id_product DESC LIMIT {n_borrar})"
            )
            conn.commit()
            st.success(f"✅ {n_borrar} products deleted successfully")


if __name__ == "__main__":
    main()
