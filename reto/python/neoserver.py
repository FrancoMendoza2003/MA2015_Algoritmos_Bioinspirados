import pandas as pd

from utils._logging import logger
from utils.neoserver.neoserver import prepare_tsp

dmatrix = pd.read_csv("../datos/02_dmatrix/dmatrix.csv")


def main(red: str):
    for i in range(1, 11):
        scenario = (
            pd.read_csv(f"../datos/03_redes/{red}/{i}.csv")
            .rename(columns={"Unnamed: 0": "index"})
            .set_index("index")
        )

        nodes = scenario.index.to_list()

        dmatrix_ = dmatrix.copy()
        dmatrix_ = dmatrix_.rename(
            columns={column: int(column) for column in dmatrix_.columns}
        )
        dmatrix_ = dmatrix_.loc[nodes, nodes].reset_index(drop=True)

        dmatrix_ = dmatrix_.rename(
            columns={column: i for i, column in enumerate(dmatrix_.columns)}
        )

        noeserver_payload = prepare_tsp(
            name=f"{red}_{i}",
            nodes=len(nodes),
            matrix=dmatrix_,
        )

        with open(f"neoserver/{red}/{i}.txt", "w") as f:
            f.write(noeserver_payload)

        print(f"{noeserver_payload}")


if __name__ == "__main__":
    red = "n200"
    main(red=red)
