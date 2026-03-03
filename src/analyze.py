import pandas as pd
from pathlib import Path

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
            ).head(5)
        )
        .reset_index(drop=True)
    )

    return df_group


if __name__ == "__main__":
    df_master = pd.read_csv(DATA_PROCESSED_PATH / "master.csv")
    print(df_master.head())

    top_5_por_categoria = top_5_mas_vendidos_categoria(df_master)
    print(top_5_por_categoria)
