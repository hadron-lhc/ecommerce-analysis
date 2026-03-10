import sqlite3
import sys
from pathlib import Path
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from streamlit_extras.add_vertical_space import add_vertical_space

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
# importar las funciones de sql_quries.py

from src.sql_queries import (
    top_5_mas_vendidos,
    clientes_mas_revenue,
    ticket_promedio_ciudad,
    mes_pico_ventas,
    clientes_sin_compras,
    tasa_recompra,
)

DATABASE_PATH = Path(__file__).parent.parent.parent / "database" / "ecommerce.db"


def grafico_top_5(df):
    df = df[df["category"] != "unknown"]
    fig = px.bar(
        df,
        x="total_unidades",
        y="name",
        color="category",
        orientation="h",
        title="TOP 5 más vendidos por categoría",
        labels={"total_unidades": "Unidades Vendidas", "name": "Producto"},
    )

    fig.update_layout(
        title={"x": 0.5, "xanchor": "center", "font": {"size": 18}},
        height=500,  # altura del gráfico
        yaxis=dict(autorange="reversed"),
    )

    st.plotly_chart(fig, use_container_width=True)


def grafico_clientes_revenue(df):
    fig = px.bar(
        df,
        x="total",
        y="name",
        orientation="h",
        title="Clientes con mayor revenue",
        labels={"total": "Revenue Total", "name": "Cliente"},
    )

    fig.update_layout(
        title={"x": 0.5, "xanchor": "center", "font": {"size": 18}},
        height=500,  # altura del gráfico
        yaxis=dict(autorange="reversed"),
    )

    st.plotly_chart(fig, use_container_width=True)


def promedio_ticket_ciudad(df):
    df = df.sort_values(by="promedio", ascending=False)
    df = df.nlargest(5, "promedio")

    fig = px.bar(
        df,
        x="city",
        y="promedio",
        orientation="v",
        title="Promedio de ticket por ciudad",
        labels={"promedio": "Promedio Ticket", "city": "Ciudad"},
        color_discrete_sequence=["#aa6EaA"],  # color personalizado para las barras
    )

    fig.update_layout(
        title={"x": 0.5, "xanchor": "center", "font": {"size": 18}},
        height=500,  # altura del gráfico
    )

    st.plotly_chart(fig, use_container_width=True)


def mes_pico_ventas_grafico(df):
    df["periodo"] = df["year"].astype(str) + "-" + df["month"].astype(str)
    fig = px.line(
        df,
        x="periodo",
        y="total",
        title="Ventas por mes",
        labels={"periodo": "Mes-Año", "total_ventas": "Total Ventas"},
    )

    fig.update_layout(
        title={"x": 0.5, "xanchor": "center", "font": {"size": 18}},
        height=500,  # altura del gráfico
    )

    st.plotly_chart(fig, use_container_width=True)


def clientes_sin_copras_grafico(df):
    porcentaje = df.iloc[0]["porcentaje"]
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=porcentaje,
            gauge={"axis": {"range": [0, 100]}},
        )
    )

    fig.update_layout(
        title={
            "x": 0.5,
            "text": "% Clientes sin compras",
            "xanchor": "center",
            "font": {"size": 18},
        },
    )

    st.plotly_chart(fig, use_container_width=True)


def tasa_recompra_grafico(df):
    fig = px.bar(
        df,
        x="category",
        y="tasa_recompra",
        text_auto=True,
        orientation="v",
        title="Tasa recompra",
        labels={"category": "Categoria", "tasa_recompra": "Tasa"},
        color_discrete_sequence=["#4d9"],
    )

    fig.update_layout(
        title={"x": 0.5, "xanchor": "center", "font": {"size": 18}},
        height=500,  # altura del gráfico
    )
    fig.update_traces(textfont_size=14, textfont_color="black")

    st.plotly_chart(fig, use_container_width=True)


def main():
    st.markdown(
        "<h1 style='text-align: center;'>Dashboard</h1>", unsafe_allow_html=True
    )
    add_vertical_space(5)

    st.set_page_config(layout="wide")

    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)

    col1, col2 = st.columns(2, gap="large")
    with col1:
        df_top_5_vendidos = top_5_mas_vendidos(conn)
        grafico_top_5(df_top_5_vendidos)
        df_ticket_promedio_ciudad = ticket_promedio_ciudad(conn)
        promedio_ticket_ciudad(df_ticket_promedio_ciudad)
        df_clientes_sin_compras = clientes_sin_compras(conn)
        clientes_sin_copras_grafico(df_clientes_sin_compras)
    with col2:
        df_clientes_revenue = clientes_mas_revenue(conn)
        grafico_clientes_revenue(df_clientes_revenue)
        df_mes_pico_ventas = mes_pico_ventas(conn)
        mes_pico_ventas_grafico(df_mes_pico_ventas)
        df_tasa_recompra = tasa_recompra(conn)
        tasa_recompra_grafico(df_tasa_recompra)

    return


if __name__ == "__main__":
    main()
