import pandas as pd
from pathlib import Path

# from config import paises_mapping
from generate_data import guardar_df

DATA_PROCESSED_PATH = Path(__file__).parent.parent / "data" / "processed"


def transformar(df_ordenes, df_clientes, df_productos):
    df_ordenes["order_date"] = pd.to_datetime(df_ordenes["order_date"])
    df_ordenes["year_month"] = df_ordenes["order_date"].dt.to_period("M")
    df_ordenes["year"] = df_ordenes["order_date"].dt.year
    df_ordenes["month"] = df_ordenes["order_date"].dt.month

    df_maestro = pd.merge(
        df_ordenes, df_clientes, left_on="client_id", right_on="id", how="left"
    )
    df_maestro = pd.merge(
        df_maestro,
        df_productos,
        left_on="product_id",
        right_on="id_product",
        how="left",
    )

    df_maestro = df_maestro[df_maestro["category"] != "unknown"]

    return df_maestro


if __name__ == "__main__":
    df_clientes = pd.read_csv(DATA_PROCESSED_PATH / "clients_clean.csv")
    df_productos = pd.read_csv(DATA_PROCESSED_PATH / "products_clean.csv")
    df_ordenes = pd.read_csv(DATA_PROCESSED_PATH / "orders_clean.csv")

    df_maestro = transformar(df_ordenes, df_clientes, df_productos)
    guardar_df(df_maestro, "master", DATA_PROCESSED_PATH)
    print(df_maestro)
    print(df_maestro.columns)
