from time import perf_counter
from pathlib import Path

from utils.logging import logger
from utils.heuristics import GreedyHeuristic
from utils.scenarios import load_all_scenarios, select_scenario

import pandas as pd


data_path = Path("..", "Documentos", "mochila_1.xlsx")


def main(df: pd.DataFrame):
    for i in range(1, 30):
        problem = select_scenario(df, i)

        solver = GreedyHeuristic.from_values(
            names=problem.columns.tolist(),
            costs=problem.loc["Peso"].tolist(),
            benefits=problem.loc["Beneficio"].tolist(),
            max_cost=700,
        )

        print(f"=== Scenario {i} ===")
        *_, exec_time = solver.solve()

        logger.info(f"Problem {i} Execution Time: {exec_time*1000}ms")


if __name__ == "__main__":
    df = load_all_scenarios(data_path)

    start = perf_counter()
    main(df)
    end = perf_counter()

    logger.info(f"Total Execution Time: {(end-start)*1000}ms\n")
