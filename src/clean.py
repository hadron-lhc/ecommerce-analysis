import pandas as pd
from pathlib import Path
from config import paises_mapping
from generate_data import guardar_df

DATA_RAW_PATH = Path(__file__).parent.parent / "data" / "raw"
DATA_PROCESSED_PATH = Path(__file__).parent.parent / "data" / "processed"


def limpiar_clientes(df_sucio):
    df = df_sucio.copy()

    df = df.drop_duplicates(subset=["id"], keep="first")
    df = df.dropna(subset=["registration_date", "active"])

    df["city"] = df["city"].fillna("unknown")
    df["name"] = df["name"].fillna("unknown")

    df["name"] = df["name"].str.strip().str.lower().str.title()
    df["email"] = df["email"].str.strip()

    df["country"] = df["country"].replace(paises_mapping)

    df["registration_date"] = pd.to_datetime(df["registration_date"], format="mixed")

    return df


def limpiar_productos(df_sucio):
    df = df_sucio.copy()

    df["name"] = df["name"].fillna("unknown")

    df["category"] = df["category"].fillna("unknown")

    df = df.drop_duplicates(subset=["id_product"], keep="first")

    df["price"] = (
        df["price"].round(2).astype(str).str.replace("$", "", regex=False).astype(float)
    )

    df["price"] = df["price"].fillna(df["price"].median())

    return df


def limpiar_ordenes(df_sucio):
    df = df_sucio.copy()

    df = df.drop_duplicates(subset=["order_id"], keep="first")

    df["unitary_price"] = (
        df["unitary_price"]
        .round(2)
        .astype(str)
        .str.replace("$", "", regex=False)
        .astype(float)
    )

    df["unitary_price"] = df["unitary_price"].fillna(df["unitary_price"].median())

    df["order_date"] = pd.to_datetime(df["order_date"], format="mixed")

    df["state"] = df["state"].fillna("unknown")

    return df


def main():
    df_clientes = pd.read_csv(DATA_RAW_PATH / "dirty_clients.csv")
    df_productos = pd.read_csv(DATA_RAW_PATH / "dirty_products.csv")
    df_ordenes = pd.read_csv(DATA_RAW_PATH / "dirty_orders.csv")

    df_clientes_limpio = limpiar_clientes(df_clientes)
    df_productos_limpio = limpiar_productos(df_productos)
    df_ordenes_limpio = limpiar_ordenes(df_ordenes)

    try:
        guardar_df(df_clientes_limpio, "clients_clean", DATA_PROCESSED_PATH)
        guardar_df(df_productos_limpio, "products_clean", DATA_PROCESSED_PATH)
        guardar_df(df_ordenes_limpio, "orders_clean", DATA_PROCESSED_PATH)

        print("CSV guardados correctamente")

    except Exception as e:
        print(f"No se pudo guardar correctaente: {e}")


if __name__ == "__main__":
    main()
