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
        SELECT
            COUNT(c.id) as total_clientes,
            COUNT(o.client_id) as con_compras,
            COUNT(c.id) - COUNT(o.client_id) as sin_compras,
            ROUND((COUNT(c.id) - COUNT(o.client_id)) * 100.0 / COUNT(c.id), 2) as porcentaje
        FROM clients c
        LEFT JOIN orders o ON o.client_id = c.id
    """

    df = pd.read_sql_query(query, conn)

    return df


def tasa_recompra(conn):
    query = """
        WITH compras_por_cliente as (
            SELECT
                category,
                client_id,
                COUNT(o.order_id) as num_compras
            FROM orders o
            JOIN products p ON p.id_product = o.product_id
            GROUP BY p.category, o.client_id
        )
    SELECT
        category,
        COUNT(client_id) as clientes_por_categoria,
        SUM(CASE WHEN num_compras > 1 THEN 1 ELSE 0 END) as clientes_recurrentes,
        ROUND(SUM(CASE WHEN num_compras > 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(client_id), 2) as tasa_recompra
    FROM compras_por_cliente
    GROUP BY category
    """

    df = pd.read_sql_query(query, conn)
    return df


def main(df_clients, df_products, df_orders):
    conn = sqlite3.connect(DATABASE_PATH / "ecommerce.db")

    df_clients.to_sql("clients", conn, if_exists="replace", index=False)
    df_products.to_sql("products", conn, if_exists="replace", index=False)
    df_orders.to_sql("orders", conn, if_exists="replace", index=False)

    return conn


if __name__ == "__main__":
    df_clients = pd.read_csv(DATA_PROCESSED_PATH / "clients_clean.csv")
    df_products = pd.read_csv(DATA_PROCESSED_PATH / "products_clean.csv")
    df_orders = pd.read_csv(DATA_PROCESSED_PATH / "orders_clean.csv")

    main(df_clients, df_products, df_orders)
