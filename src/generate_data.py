import pandas as pd
from faker import Faker
import random
import numpy as np
from pathlib import Path
from synthetic_noise import ensuciar_clientes, ensuciar_productos, ensuciar_ordenes
from config import (
    spanish_speaking_countries,
    categorias,
    nombres_por_categoria,
    precios_por_categoria,
)

fake = Faker("es_ES")

DATA_RAW_PATH = Path(__file__).parent.parent / "data" / "raw"


def generar_clientes(n=200):
    clientes = [
        {
            "id": i,
            "name": fake.name(),
            "email": fake.email(),
            "city": fake.city(),
            "country": random.choice(spanish_speaking_countries),
            "registration_date": fake.date_between(start_date="-5y", end_date="today"),
            "active": random.choice([0, 1]),
        }
        for i in range(n)
    ]

    df_clientes = pd.DataFrame(clientes)

    return df_clientes


def generar_productos(n=50):
    productos = []
    for i in range(n):
        categoria = random.choice(categorias)
        nombre = random.choice(nombres_por_categoria[categoria])
        min_precio, max_precio = precios_por_categoria[categoria]
        productos.append(
            {
                "id_product": i,
                "category": categoria,
                "name": nombre,
                "price": round(random.uniform(min_precio, max_precio), 2),
                "stock": fake.random_int(min=0, max=100),
            }
        )

    df_productos = pd.DataFrame(productos)

    return df_productos


def generar_ordenes(df_productos, df_clientes, n=500):
    ordenes = []

    for i in range(n):
        product_id = fake.random_int(min=0, max=len(df_productos) - 1)
        client_id = fake.random_int(min=0, max=len(df_clientes) - 1)
        precio_unitario = df_productos.loc[product_id, "price"]
        cantidad = fake.random_int(min=1, max=5)

        ordenes.append(
            {
                "order_id": i,
                "client_id": client_id,
                "product_id": product_id,
                "unitary_price": precio_unitario,
                "mount": cantidad,
                "total": precio_unitario * cantidad,
                "order_date": fake.date_between(start_date="-5m", end_date="today"),
                "state": random.choice(["complete", "pending", "canceled"]),
            }
        )

    df_ordenes = pd.DataFrame(ordenes)

    return df_ordenes


def guardar_df(df, nombre_archivo, path):
    path.mkdir(parents=True, exist_ok=True)
    filepath = path / f"{nombre_archivo}.csv"
    df.to_csv(filepath, index=False)


def main():
    # Data-sets limpios
    df_clientes = generar_clientes()
    df_productos = generar_productos()
    df_ordenes = generar_ordenes(df_productos, df_clientes)

    # Data-sets sucios
    df_productos_sucios = ensuciar_productos(df_productos)
    df_clientes_sucios = ensuciar_clientes(df_clientes)
    df_ordenes_sucios = ensuciar_ordenes(df_ordenes)

    df_sucios = [
        (df_productos_sucios, "dirty_products"),
        (df_clientes_sucios, "dirty_clients"),
        (df_ordenes_sucios, "dirty_orders"),
    ]

    for df, nombre in df_sucios:
        guardar_df(df, nombre, DATA_RAW_PATH)


if __name__ == "__main__":
    main()
