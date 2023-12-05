import pandas as pd

TSP_FORMAT_FILE = """
NAME: {name}
COMMENT: TSP problem with {nodes} nodes and distance matrix
TYPE: TSP
DIMENSION: {nodes}
EDGE_WEIGHT_TYPE: EXPLICIT
EDGE_WEIGHT_FORMAT: FULL_MATRIX
EDGE_WEIGHT_SECTION
{matrix}
EOF
"""


def prepare_tsp(name: str, nodes: int, matrix: pd.DataFrame) -> str:
    # columns = matrix.columns + 1
    # matrix.index = matrix.index + 1
    # columns_str = map(str, columns.to_list())
    # matrix_str: str = "0 " + " ".join(columns_str) + "\n"

    matrix_str = ""

    for row in matrix.iterrows():
        for val in row[1]:
            matrix_str += str(int(val * 10_000)).ljust(10)

        matrix_str += "\n"

    return TSP_FORMAT_FILE.format(
        name=name,
        nodes=nodes,
        matrix=matrix_str,
    )
