import pandas as pd
import sqlite3
from pathlib import Path
import streamlit as st
import sys

from streamlit_extras.add_vertical_space import add_vertical_space

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.generate_data import generar_clientes
from src.clean import limpiar_clientes
from app.components.sidebar import sidebar

DATABASE_PATH = Path(__file__).parent.parent.parent / "database" / "ecommerce.db"


def obtener_clientes(conn):
    query = """
        SELECT
            name,
            city,
            country,
            email,
            registration_date,
            active
        FROM
            clients
    """
    df = pd.read_sql_query(query, conn)
    return df


def main():
    sidebar()
    st.markdown("<h1 style='text-align: center;'>Clients</h1>", unsafe_allow_html=True)
    add_vertical_space(3)

    st.set_page_config(layout="wide")
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    df_clients = obtener_clientes(conn)
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        countries = ["All"] + sorted(df_clients["country"].unique().tolist())
        country_selected = st.selectbox("Filter by country", countries)

    with col2:
        if country_selected != "All":
            df_filtered = df_clients[df_clients["country"] == country_selected]
        else:
            df_filtered = df_clients

        cities = ["All"] + sorted(df_filtered["city"].unique().tolist())
        city_selected = st.selectbox("Filter by city", cities)

    if country_selected != "All":
        df_filtered = df_filtered[df_filtered["country"] == country_selected]

    if city_selected != "All":
        df_filtered = df_filtered[df_filtered["city"] == city_selected]

    st.dataframe(df_filtered)

    st.divider()
    st.subheader("Add clients")

    tab1, tab2, tab3 = st.tabs(["Generate Random", "Add Manually", "Delete"])

    with tab1:
        n = st.number_input(
            "Number of clients to generate", min_value=1, max_value=50, value=1
        )
        if st.button("Generate clients"):
            df_nuevos = generar_clientes(n)
            df_nuevos_limpios = limpiar_clientes(df_nuevos)
            df_nuevos_limpios.to_sql("clients", conn, if_exists="append", index=False)
            st.success(f"✅ {n} clients generated successfully")

    with tab2:
        with st.form("form_client"):
            nombre = st.text_input("Name")
            email = st.text_input("Email")
            pais = st.selectbox(
                "Country", sorted(df_clients["country"].unique().tolist())
            )
            ciudad = st.selectbox(
                "City", sorted(df_clients["city"].unique().tolist())
            )
            activo = st.selectbox("Active", [1, 0])
            submitted = st.form_submit_button("Save client")

            if submitted:
                conn.execute(
                    """
                    INSERT INTO clients (name, email, city, country, active, registration_date)
                    VALUES (?, ?, ?, ?, ?, ?)
                """,
                    (
                        nombre,
                        email,
                        ciudad,
                        pais,
                        activo,
                        pd.Timestamp.today().strftime("%Y-%m-%d"),
                    ),
                )
                conn.commit()
                st.success(f"✅ Client {nombre} added successfully")
    with tab3:
        n_borrar = st.number_input(
            "Number of clients to delete",
            min_value=1,
            max_value=50,
            value=1,
        )
        if st.button("Delete clients"):
            conn.execute(
                f"DELETE FROM clients WHERE id IN (SELECT id FROM clients ORDER BY id DESC LIMIT {n_borrar})"
            )
            conn.commit()
            st.success(f"✅ {n_borrar} clients deleted successfully")


if __name__ == "__main__":
    main()
