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

    df_clientes_sucios = ensuciar_clientes(df_clientes)

    return df_clientes_sucios


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

    df_profuctos_sucios = ensuciar_productos(df_productos)

    return df_profuctos_sucios


if __name__ == "__main__":
    df_clientes = generar_clientes()
    df_productos = generar_productos()
    print(df_clientes.head())
    print()
    print(df_productos.head())
