import pandas as pd
from faker import Faker
import random
import numpy as np
from synthetic_noise import ensuciar_clientes, ensuciar_productos
from config import (
    spanish_speaking_countries,
    categorias,
    nombres_por_categoria,
    precios_por_categoria,
)

fake = Faker("es_ES")


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


if __name__ == "__main__":
    # Data-sets limpios
    df_clientes = generar_clientes()
    df_productos = generar_productos()

    # Data-sets sucios
    df_profuctos_sucios = ensuciar_productos(df_productos)
    df_clientes_sucios = ensuciar_clientes(df_clientes)

    # Generar ordenes con data-sets limpios
    df_ordenes = generar_ordenes(df_productos, df_clientes)

    print(df_clientes.head())
    print()
    print(df_productos.head())
    print()
    print(df_ordenes.head())
