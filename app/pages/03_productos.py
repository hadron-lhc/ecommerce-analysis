import pandas as pd
import sqlite3
from pathlib import Path
import streamlit as st
import sys

from streamlit_extras.add_vertical_space import add_vertical_space

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.generate_data import generar_productos
from src.clean import limpiar_productos

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
    st.markdown(
        "<h1 style='text-align: center;'>Productos</h1>", unsafe_allow_html=True
    )
    add_vertical_space(3)

    st.set_page_config(layout="wide")
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)

    df_productos = obtener_productos(conn)

    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        categoria = ["Todas"] + sorted(df_productos["category"].unique().tolist())
        categoria_seleccionada = st.selectbox("Filtrar por categoria", categoria)

    with col2:
        min_precio = 0
        max_precio = int(df_productos["price"].max())

        rango_precio = st.slider(
            "Selecciona el rango de precio:",
            min_value=min_precio,
            max_value=max_precio,
            value=(min_precio, max_precio),  # Valor por defecto (min, max)
        )

        df_filtrado = df_productos[
            (df_productos["price"] >= rango_precio[0])
            & (df_productos["price"] <= rango_precio[1])
        ]

    if categoria_seleccionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado["category"] == categoria_seleccionada]

    st.dataframe(df_filtrado)

    st.divider()  # línea separadora
    st.subheader("Agregar productos")

    tab1, tab2, tab3 = st.tabs(["Generar aleatorios", "Agregar manualmente", "Borrar"])

    with tab1:
        n = st.number_input(
            "Cantidad de clientes a generar", min_value=1, max_value=50, value=1
        )
        if st.button("Generar productos"):
            df_nuevos = generar_productos(n)
            df_nuevos_limpios = limpiar_productos(df_nuevos)
            df_nuevos_limpios.to_sql("products", conn, if_exists="append", index=False)
            st.success(f"✅ {n} producots generados correctamente")

    with tab2:
        with st.form("form_cliente"):
            nombre = st.text_input("Nombre")
            categoria = st.selectbox(
                "Categoria", sorted(df_productos["category"].unique().tolist())
            )
            precio = st.number_input("precio")

            submitted = st.form_submit_button("Guardar producto")

            if submitted:
                # insertar en la DB
                conn.execute(
                    """
                    INSERT INTO products (category, name, price)
                    VALUES (?, ?, ?)
                """,
                    (categoria, nombre, precio),
                )
                conn.commit()
                st.success(f"✅ Producto {nombre} agregado correctamente")
    with tab3:
        n_borrar = st.number_input(
            "Cantidad de productos a borrar",
            min_value=1,
            max_value=50,
            value=1,
        )
        if st.button("Borrar productos"):
            conn.execute(
                f"DELETE FROM products WHERE id_product IN (SELECT id_product FROM products ORDER BY id_product DESC LIMIT {n_borrar})"
            )
            conn.commit()
            st.success(f"✅ {n_borrar} productos borrados correctamente")


if __name__ == "__main__":
    main()
