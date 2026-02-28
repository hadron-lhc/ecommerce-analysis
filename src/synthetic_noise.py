import random
import numpy as np
import pandas as pd


def agregar_nulos(series, frac_null=0.1):
    series = series.copy()
    idx_null = series.sample(frac=frac_null).index
    series.loc[idx_null] = np.nan

    return series


def agregar_duplicados(df, frac_duplicate=0.05):
    df = df.copy()

    duplicados = df.sample(frac=frac_duplicate)
    df = pd.concat([df, duplicados], ignore_index=True)

    return df


def ensuciar_precio(series, frac_null=0.05, frac_noise=0.15):
    series = series.copy()

    idx_null = series.sample(frac=frac_null).index
    series.loc[idx_null] = np.nan

    idx_noise = series.sample(frac=frac_noise).index
    series.loc[idx_noise] = series.loc[idx_noise].apply(
        lambda x: x * random.uniform(0.8, 1.2) if pd.notna(x) else x
    )

    return series


def cambiar_mayusculas_minusculas(series, frac=0.2):
    idx = series.sample(frac=frac).index
    series = series.copy()
    series.loc[idx] = series.loc[idx].apply(
        lambda x: x.upper() if random.random() > 0.5 else x.lower()
    )
    return series


def cambiar_formato_fecha(series, frac=0.1, formato="%d/%m/%Y"):
    idx = series.sample(frac=frac).index
    series = series.copy()
    series.loc[idx] = series.loc[idx].apply(
        lambda x: (
            pd.Timestamp(x).strftime(formato)
            if pd.notna(x) and x != "2024/99/99"
            else x
        )
    )
    return series


def ensuciar_clientes(df_limpio):
    df = df_limpio.copy()

    df["name"] = cambiar_mayusculas_minusculas(df["name"], frac=0.2)

    idx_email = df.sample(frac=0.15).index
    df.loc[idx_email, "email"] = df.loc[idx_email, "email"].apply(lambda x: f"  {x}  ")

    df["city"] = agregar_nulos(df["city"], frac_null=0.1)

    idx_country = df.sample(frac=0.1).index
    df.loc[idx_country, "country"] = df.loc[idx_country, "country"].replace(
        {"Spain": "ESP", "Nicaragua": "NIC"}
    )

    df["registration_date"] = cambiar_formato_fecha(df["registration_date"], frac=0.1)

    df = agregar_duplicados(df)

    return df


def ensuciar_productos(df_limpio):
    df = df_limpio.copy()

    df["name"] = cambiar_mayusculas_minusculas(df["name"], frac=0.2)

    df["price"] = ensuciar_precio(df["price"], frac_null=0.05, frac_noise=0.15)

    df["category"] = agregar_nulos(df["category"], frac_null=0.08)

    df = agregar_duplicados(df)

    return df


def ensuciar_ordenes(df_limmpio):
    df = df_limmpio.copy()

    df["unitary_price"] = ensuciar_precio(
        df["unitary_price"], frac_null=0.05, frac_noise=0.15
    )

    df["order_date"] = cambiar_formato_fecha(df["order_date"], frac=0.1)

    df["state"] = agregar_nulos(df["state"], frac_null=0.08)

    df = agregar_duplicados(df)

    return df


if __name__ == "__main__":
    print("Archivo para ensuciar data")
