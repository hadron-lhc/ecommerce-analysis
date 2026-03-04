import pandas as pd
from pathlib import Path

from pandas.core import groupby

DATA_PROCESSED_PATH = Path(__file__).parent.parent / "data" / "processed"


def top_5_mas_vendidos_categoria(df):
    df = df.copy()

    df_group = (
        df.groupby(["category", "name_y"])["mount"]
        .sum()
        .reset_index()
        .groupby("category")
        .apply(
            lambda x: x.sort_values(
                "mount",
                ascending=False,
            ).head(5),
            include_groups=False,
        )
        .reset_index(drop=True)
    )

    return df_group


def clientes_mas_revenue(df):
    df = df.copy()

    df_group = (
        df.groupby(["client_id", "name_x"])["total"]
        .sum()
        .reset_index()
        .sort_values(by="total", ascending=False)
        .head(10)
        .reset_index(drop=True)
    )

    return df_group


def ticket_promedio_ciudad(df):
    df = df.copy()

    df = df[(df["country"] != "unknown") & (df["city"] != "unknown")]

    df_group = df.groupby(["country", "city"])["total"].apply(
        lambda x: x.mean().round(2)
    )

    return df_group


def mes_pico_ventas(df):
    df = df.copy()

    df["order_date"] = pd.to_datetime(df["order_date"], format="mixed")

    df_group = (
        df.groupby(df["order_date"].dt.to_period("M"))["total"].sum().reset_index()
    )

    df_group["year"] = df_group["order_date"].dt.year

    df_group = (
        df_group.groupby("year")
        .apply(lambda x: x.loc[x["total"].idxmax()], include_groups=False)
        .reset_index(drop=True)
    )

    return df_group


def clientes_sin_compras(df_master, df_clientes):
    df = df_master.copy()

    total_clientes = len(df_clientes)
    clientes_compras = len(df.drop_duplicates(subset="client_id"))

    clientes_sin_compras = total_clientes - clientes_compras
    porcentaje = (clientes_sin_compras / total_clientes) * 100

    return round(porcentaje, 2)


def tasa_recompra_categoria(df_master):
    df = df_master.copy()

    df = df[df["category"] != "unknown"]
    df_group = (
        df.groupby(["category", "client_id"]).size().reset_index(name="num_compras")
    )

    def calcular_tasa(group):
        total_clientes = len(group)
        recurrentes = (group["num_compras"] > 1).sum()
        return (recurrentes / total_clientes) * 100

    tasa_recompra = (
        df_group.groupby("category").apply(calcular_tasa, include_groups=False).round(2)
    )

    print(tasa_recompra)


if __name__ == "__main__":
    df_master = pd.read_csv(DATA_PROCESSED_PATH / "master.csv")
    df_clientes = pd.read_csv(DATA_PROCESSED_PATH / "clients_clean.csv")

    top_5_por_categoria = top_5_mas_vendidos_categoria(df_master)
    clientes_mas_revenue = clientes_mas_revenue(df_master)
    ticket_promedio_ciudad = ticket_promedio_ciudad(df_master)
    mes_pico_ventas = mes_pico_ventas(df_master)
    procentaje_clientes_sin_compras = clientes_sin_compras(df_master, df_clientes)

    tasa_recompra_categoria(df_master)
