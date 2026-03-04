import sqlite3
import pandas as pd
from pathlib import Path

DATA_PROCESSED_PATH = Path(__file__).parent.parent / "data" / "processed"
DATABASE_PATH = Path(__file__).parent.parent / "database"


def mostrar_datos(conn, df_name):
    query = "SELECT * FROM " + df_name

    df = pd.read_sql_query(query, conn)

    print(df.head())


def top_5_mas_vendidos(conn):
    query = """
    WITH ventas_por_producto AS (
        SELECT
            p.category,
            p.name,
            SUM(o.mount) as total_unidades,
            ROW_NUMBER() OVER (PARTITION BY p.category ORDER BY SUM(o.mount) DESC) as rn
        FROM products p
        JOIN orders o ON o.product_id = p.id_product
        GROUP BY p.category, p.name
    )
    SELECT category, name, total_unidades
    FROM ventas_por_producto
    WHERE rn <= 5
    ORDER BY category, total_unidades DESC
    """

    df = pd.read_sql_query(query, conn)
    return df


def clientes_mas_revenue(conn):
    query = """
    SELECT
        c.name,
        SUM(o.total) as total
    FROM clients c
    JOIN orders o ON o.client_id = c.id
    GROUP BY c.name
    ORDER BY total DESC
    LIMIT 10
    """

    df = pd.read_sql_query(query, conn)
    return df


def ticket_promedio_ciudad(conn):
    query = """
        SELECT
            c.city,
            ROUND(AVG(o.total)) as promedio
        FROM clients c
        JOIN orders o ON o.client_id = c.id
        WHERE c.city != 'unknown'
        GROUP BY c.city
    """

    df = pd.read_sql_query(query, conn)
    return df


def mes_pico_ventas(conn):
    query = """
    WITH ventas_por_mes AS (
        SELECT
            strftime('%Y', o.order_date) as year,
            strftime('%m', o.order_date) as month,
            SUM(o.total) as total,
            ROW_NUMBER() OVER (PARTITION BY strftime('%Y', order_date) ORDER BY SUM(total) DESC) as rn
        FROM
            orders o
        GROUP BY strftime('%Y', o.order_date), strftime('%m', o.order_date)
    )
    SELECT
       year, month, total
    FROM
        ventas_por_mes
    WHERE
        rn = 1
    """

    df = pd.read_sql_query(query, conn)

    return df


def clientes_sin_compras(conn):
    query = """
    """
    pass


def main():
    conn = sqlite3.connect(DATABASE_PATH / "ecommerce.db")

    df_clients.to_sql("clients", conn, if_exists="replace", index=False)
    df_products.to_sql("products", conn, if_exists="replace", index=False)
    df_orders.to_sql("orders", conn, if_exists="replace", index=False)

    dataframes = {"clients": df_clients, "products": df_products, "orders": df_orders}

    top_5_categorias = top_5_mas_vendidos(conn)
    top_10_clientes = clientes_mas_revenue(conn)
    promedio_ciudad = ticket_promedio_ciudad(conn)
    top_meses = mes_pico_ventas(conn)


if __name__ == "__main__":
    df_clients = pd.read_csv(DATA_PROCESSED_PATH / "clients_clean.csv")
    df_products = pd.read_csv(DATA_PROCESSED_PATH / "products_clean.csv")
    df_orders = pd.read_csv(DATA_PROCESSED_PATH / "orders_clean.csv")

    main()
