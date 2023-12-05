from pathlib import Path

from utils.gams import write_gams
from utils.logging import logger
from utils.scenarios import load_all_scenarios, select_scenario

import pandas as pd

data_path = Path("..", "Documentos", "mochila_1.xlsx")
file_path = "gamsact1.txt"


def main(df: pd.DataFrame):
    for scenario in range(1, 30):
        problem = select_scenario(df, scenario=scenario)

        gams = write_gams(
            problem_id=scenario,
            costs=problem.loc["Peso"].tolist(),
            benefits=problem.loc["Beneficio"].tolist(),
            max_cost=700,
        )

        logger.info(f"Problem {scenario}")
        print(gams)
        with open(file_path, 'a') as file:
            file.write(f"Problem {scenario} \n")
            file.write(gams)
            file.write("\n ====================================================== \n")


if __name__ == "__main__":
    df = load_all_scenarios(data_path)

    main(df)
