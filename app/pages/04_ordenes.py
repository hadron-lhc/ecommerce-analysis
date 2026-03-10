import pandas as pd
import sqlite3
from pathlib import Path
import streamlit as st
import sys

from streamlit_extras.add_vertical_space import add_vertical_space

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.generate_data import generar_ordenes
from src.clean import limpiar_ordenes

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
    df = pd.read_sql_query(query, conn)
    return df


def main():
    st.markdown("<h1 style='text-align: center;'>Ordenes</h1>", unsafe_allow_html=True)
    add_vertical_space(3)

    st.set_page_config(layout="wide")
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)

    df_ordenes = obtener_ordenes(conn)
    df_ordenes["fecha_orden"] = pd.to_datetime(df_ordenes["fecha_orden"])

    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        estado = ["Todos"] + df_ordenes["estado"].unique().tolist()
        estado_seleccionado = st.selectbox("Filtrar por estado", estado)

    with col2:
        fecha_inicio = df_ordenes["fecha_orden"].min().date()
        fecha_fin = df_ordenes["fecha_orden"].max().date()

        rango = st.date_input(
            "Rango de fechas: ", value=(fecha_inicio, fecha_fin), key="filtro_fecha"
        )

        if isinstance(rango, tuple) and len(rango) == 2:
            inicio = pd.Timestamp(rango[0])
            fin = pd.Timestamp(rango[1])
        elif isinstance(rango, tuple) and len(rango) == 1:
            inicio = pd.Timestamp(rango[0])
            fin = pd.Timestamp(df_ordenes["fecha_orden"].max())
        else:
            inicio = pd.Timestamp(df_ordenes["fecha_orden"].min())
            fin = pd.Timestamp(df_ordenes["fecha_orden"].max())

        df_filtrado = df_ordenes[df_ordenes["fecha_orden"].between(inicio, fin)]

    if estado_seleccionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["estado"] == estado_seleccionado]

    df_filtrado = df_filtrado.copy()
    df_filtrado["fecha_orden"] = df_filtrado["fecha_orden"].dt.date

    st.dataframe(df_filtrado)


if __name__ == "__main__":
    main()
