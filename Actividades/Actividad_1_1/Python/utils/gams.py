from numbers import Number
from utils.logging import logger


def write_gams(
    problem_id: int,
    benefits: list[Number],
    costs: list[Number],
    max_cost: Number,
    opt_ctr: float | str = "0.00001",
) -> str:
    assert (
        len(benefits) == len(costs),
        f"Debe haber la misma cantidad de beneficios que de costos.\n# beneficios {len(benefits)}\n#{len(costs)}",
    )

    cost_param = "\n".join(f"{i} {p}" for i, p in enumerate(costs, start=1))
    benefits_param = "\n".join(f"{i} {b}" for i, b in enumerate(benefits, start=1))

    program_str = f"""option OptCR = {str(opt_ctr)};
set
i /1*{len(benefits)}/;

Variable
z;

binary variable
x(i);

Parameter
p(i)/
{cost_param}
/;

Parameter
b(i)/
{benefits_param}
/;

equations
FO
r1;

FO.. z =e= sum(i, x(i)*b(i));

r1.. sum(i,  x(i)*p(i)) =l= {max_cost};

model pregunta{problem_id}_cargero /all/;
solve pregunta{problem_id}_cargero using mip max z;
"""
    return program_str
