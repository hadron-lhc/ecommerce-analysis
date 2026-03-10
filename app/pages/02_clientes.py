import pandas as pd
import sqlite3
from pathlib import Path
import streamlit as st
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.generate_data import generar_clientes

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
    st.set_page_config(layout="wide")
    conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    df_clientes = obtener_clientes(conn)
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        paises = ["Todos"] + sorted(df_clientes["country"].unique().tolist())
        pais_seleccionado = st.selectbox("Filtrar por país", paises)

    with col2:
        # Filtrar ciudades según el país seleccionado
        if pais_seleccionado != "Todos":
            df_filtrado = df_clientes[df_clientes["country"] == pais_seleccionado]
        else:
            df_filtrado = df_clientes

        ciudades = ["Todas"] + sorted(df_filtrado["city"].unique().tolist())
        ciudad_seleccionada = st.selectbox("Filtrar por ciudad", ciudades)

    # Aplicar filtros
    if pais_seleccionado != "Todos":
        df_filtrado = df_filtrado[df_filtrado["country"] == pais_seleccionado]

    if ciudad_seleccionada != "Todas":
        df_filtrado = df_filtrado[df_filtrado["city"] == ciudad_seleccionada]

    st.dataframe(df_filtrado)

    st.divider()  # línea separadora
    st.subheader("Agregar clientes")

    tab1, tab2, tab3 = st.tabs(["Generar aleatorios", "Agregar manualmente", "Borrar"])

    with tab1:
        n = st.number_input(
            "Cantidad de clientes a generar", min_value=1, max_value=50, value=1
        )
        if st.button("Generar clientes"):
            df_nuevos = generar_clientes(n)
            df_nuevos.to_sql("clients", conn, if_exists="append", index=False)
            st.success(f"✅ {n} clientes generados correctamente")

    with tab2:
        with st.form("form_cliente"):
            nombre = st.text_input("Nombre")
            email = st.text_input("Email")
            pais = st.selectbox(
                "País", sorted(df_clientes["country"].unique().tolist())
            )
            ciudad = st.selectbox(
                "Ciudad", sorted(df_clientes["city"].unique().tolist())
            )
            activo = st.selectbox("Activo", [1, 0])
            submitted = st.form_submit_button("Guardar cliente")

            if submitted:
                # insertar en la DB
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
                st.success(f"✅ Cliente {nombre} agregado correctamente")
    with tab3:
        n_borrar = st.number_input(
            "Cantidad de clientes a borrar",
            min_value=1,
            max_value=50,
            value=1,
        )
        if st.button("Borrar clientes"):
            conn.execute(
                f"DELETE FROM clients WHERE id IN (SELECT id FROM clients ORDER BY id DESC LIMIT {n_borrar})"
            )
            conn.commit()
            st.success(f"✅ {n_borrar} clientes borrados correctamente")


if __name__ == "__main__":
    main()
