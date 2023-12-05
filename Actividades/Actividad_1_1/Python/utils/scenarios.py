import pandas as pd
import numpy as np

from utils.logging import logger


def load_all_scenarios(path: str) -> pd.DataFrame:
    df = pd.read_excel(path).drop("Contenedor", axis=1)

    cols = [f"c{i}" for i in range(1, 21)]
    df.columns = cols
    df = df.dropna(how="all")
    df = (
        df[~df["c1"].str.contains("c", na=False)]
        .astype("float64")
        .reset_index(drop=True)
    )
    df.loc[:, "problem"] = np.repeat(np.arange(1, df.shape[0] // 2 + 1), 2)
    df = df[["problem"] + cols]
    return df


def select_scenario(df: pd.DataFrame, scenario: int) -> pd.DataFrame:
    df = (
        df[df["problem"] == scenario]
        .drop("problem", axis=1)
        .dropna(axis=1)
        .set_index(pd.Series(["Peso", "Beneficio"]))
    )

    df.loc["Beneficio"] = df.loc["Beneficio"] * df.loc["Peso"]

    return df
