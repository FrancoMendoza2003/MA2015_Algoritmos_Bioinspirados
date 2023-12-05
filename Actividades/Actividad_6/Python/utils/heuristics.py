import sys
import random

if ".." not in sys.path:
    sys.path.append("../")

import pandas as pd
import numpy as np

from itertools import product
from dataclasses import dataclass, field
from numbers import Number
from time import perf_counter, sleep
from copy import deepcopy

from utils._logging import logger


@dataclass
class Job:
    index: int
    time_completion: int
    time_limit: int
    ret_cost_factor: int
    pen_cost_factor: int
    # cost: int = field(init=False)

    # def __post_init__(self):
    #     self.cost: int = self.ret_cost + self.pen_cost


@dataclass
class JobStep:
    job_1: Job
    job_2: Job
    visited: bool
    order: int
    name: str = field(init=False)

    def __post_init__(self):
        self.name = f"{self.job_1.index}{self.job_2.index}"

        self.time_completion = self.job_1.time_completion
        self.time_limit = self.job_1.time_limit
        self.ret_cost_factor = self.job_1.ret_cost_factor
        self.pen_cost_factor = self.job_1.pen_cost_factor

    def _calculate_retention_time(
        self,
        current_time: int,
    ) -> int:
        # print(
        #     f"RETENTION --- ID: {self.name}->{current_time}:{self.time_limit} = {self.time_limit - current_time}"
        # )
        return self.time_limit - current_time

    def _calculate_time_delay(
        self,
        current_time: int,
    ) -> int:
        # print(
        #     f"PENALIZATION --- ID: {self.name}->{current_time}:{self.time_limit} = {current_time - self.time_limit}"
        # )
        return current_time - self.time_limit

    def _calculate_retention_cost(
        self,
        time_retention: int,
    ) -> int:
        return max(0, time_retention) * self.ret_cost_factor

    def _calculate_penalization_cost(
        self,
        time_delay: int,
    ) -> int:
        return max(0, time_delay) * self.pen_cost_factor

    def _switch_visited(self):
        self.visited = bool(True - self.visited)


# %%


class BinaryChromosome:
    def __init__(self, id: int, gene: list[JobStep]):
        self.id = id
        self.gene = gene
        self.visited_steps = self._get_visited_jobsteps()
        self.num_steps = len(self.visited_steps)

        self.cost = self._calculate_gene_cost()

    @classmethod
    def from_dataframe(
        cls,
        id: int,
        scenario: pd.DataFrame,
    ):
        dummy_gene = cls._generate_dummy_gene(scenario=scenario)

        first_index: int = random.choices(scenario.index)[0]
        from_index = deepcopy(first_index)

        possible_destinations = deepcopy(scenario.index.to_list())
        possible_destinations.remove(from_index)

        iterations = range(1, len(possible_destinations) + 1)
        num_edges = len(deepcopy(possible_destinations))
        for i in iterations:
            if i == (num_edges + 1):
                break

            to_index: int = random.choices(possible_destinations)[0]

            job_step_name = f"{from_index}{to_index}"
            index, job_step = cls._get_jobstep(job_step_name, gene=dummy_gene)

            dummy_gene[index].visited = True
            dummy_gene[index].order = i

            from_index = deepcopy(to_index)
            possible_destinations.remove(from_index)

        final_id, final_step = cls._get_jobstep(
            f"{to_index}{first_index}", gene=dummy_gene
        )

        dummy_gene[final_id].visited = True
        dummy_gene[final_id].order = i + 1

        return cls(id, dummy_gene)

    @staticmethod
    def _generate_dummy_gene(scenario: pd.DataFrame):
        scenario = pd.DataFrame(
            data={
                "Job": [1, 2, 3, 4, 5],
                "t_i": [10, 8, 6, 7, 4],
                "d_i": [15, 20, 10, 30, 12],
                "h_i": [3, 2, 5, 4, 6],
                "c_i": [10, 22, 10, 8, 15],
            },
        ).set_index("Job")

        possible_destinations = deepcopy(scenario.index.to_list())

        possible_steps = [
            (from_, to_)
            for from_, to_ in [*product(possible_destinations, possible_destinations)]
            if from_ != to_
        ]

        gene: list[JobStep] = list()
        for from_, to_ in possible_steps:
            job_from = Job(
                index=from_,
                time_completion=scenario.loc[from_, "t_i"],
                time_limit=scenario.loc[from_, "d_i"],
                ret_cost_factor=scenario.loc[from_, "h_i"],
                pen_cost_factor=scenario.loc[from_, "c_i"],
            )
            job_to = Job(
                index=to_,
                time_completion=scenario.loc[to_, "t_i"],
                time_limit=scenario.loc[to_, "d_i"],
                ret_cost_factor=scenario.loc[to_, "h_i"],
                pen_cost_factor=scenario.loc[to_, "c_i"],
            )

            job_step = JobStep(job_1=job_from, job_2=job_to, visited=False, order=-1)

            gene.append(job_step)

        return gene

    @staticmethod
    def _valid_step(step: JobStep) -> bool:
        from_ = step.name[0]
        to_ = step.name[1]
        if from_ == to_:
            return False
        else:
            return True

    def _valid_gene(self, visited_jobsteps: list[JobStep]) -> bool:
        logger.debug(f"{[step.name for step in visited_jobsteps]=}")

        froms_ = pd.Series([step.name[0] for step in visited_jobsteps])
        tos_ = pd.Series([step.name[1] for step in visited_jobsteps])

        if len(set(froms_)) != len(froms_):
            return False

        if len(set(tos_)) != len(tos_):
            return False

        if len(set(froms_)) != self.num_steps:
            return False

        if len(set(tos_)) != self.num_steps:
            return False

        # if froms_.value_counts().sort_index().iloc[0] != 1:
        #     return False

        # if froms_.value_counts().sort_index().iloc[-1] != 1:
        #     return False

        prev_jobstep = visited_jobsteps[0]
        for current_jobstep in visited_jobsteps[1:]:
            if prev_jobstep.name[1] != current_jobstep.name[0]:
                return False

            prev_jobstep = deepcopy(current_jobstep)

        return True

    def _select_random_order(self):
        visited_steps = self._get_visited_jobsteps()

        start_index: int = random.choices(range(0, len(visited_steps)))[0]

        start_point = visited_steps.pop(start_index)

        self.path = {0: start_point}

        pos = 1
        for _ in visited_steps:
            next_step = self._search_next_step(start_point)

            if next_step in self.path.values():
                break

            self.path.update(
                {
                    pos: next_step,
                }
            )

            pos += 1
            start_point = next_step

        self.print_path()

    def print_path(self):
        print("\nSOLUTION:\n------")
        for i, node in self.path.items():
            if i + 1 != len(self.path):
                print(f"{node.name} --> ", end="")
            else:
                print(node.name)

    @staticmethod
    def _get_jobstep(name: str, gene: list[JobStep]):
        for index, step in enumerate(gene):
            if step.name == name:
                return index, step

    def _search_next_step(self, start_point: JobStep) -> JobStep:
        to_ = start_point.name[1]

        for step in self.visited_steps:
            if to_ == step.name[0]:
                return step

        raise Exception(
            f"There is another valid step from {start_point.name} in possible steps {[step.name for step in self.visited_steps]}"
        )

    def _calculate_gene_cost(self):
        current_time = self.visited_steps[0].time_completion

        time_delay = self.visited_steps[0]._calculate_time_delay(current_time)
        time_retention = self.visited_steps[0]._calculate_retention_time(current_time)

        ret_cost = self.visited_steps[0]._calculate_retention_cost(time_retention)
        pen_cost = self.visited_steps[0]._calculate_penalization_cost(time_delay)

        self.accumulated_time = [current_time]
        self.retention_cost_list = [ret_cost]
        self.penalization_cost_list = [pen_cost]

        for step in self.visited_steps[1:]:
            current_time += step.time_completion

            time_delay = step._calculate_time_delay(current_time)
            time_retention = step._calculate_retention_time(current_time)

            ret_cost += step._calculate_retention_cost(time_retention)
            pen_cost += step._calculate_penalization_cost(time_delay)

            self.accumulated_time.append(current_time)
            self.retention_cost_list.append(ret_cost)
            self.penalization_cost_list.append(pen_cost)

        return ret_cost + pen_cost

    def _get_visited_jobsteps(self) -> list[JobStep]:
        job_steps = [job_step for job_step in self.gene if job_step.visited]
        return sorted(job_steps, key=lambda jobstep: jobstep.order)

    def _get_num_visited_jobsteps(self) -> int:
        return len([job_step for job_step in self.gene if job_step.visited])

    def _switch_visited_jobstep(self, job_step_name: str):
        for job_step in self.gene:
            if job_step.name == job_step_name:
                job_step.visited = bool(True - job_step.visited)
                break

    def print_gene(self):
        for job_step in self.gene:
            logger.info(job_step)

    def __repr__(self) -> str:
        return f"""
{"ID".ljust(10)}: {self.id}
{"Jobs Done".ljust(10)}: {[step.name for step in self.visited_steps]}
{"Cost".ljust(10)}: {self._calculate_gene_cost()}
"""


# %%
# job_1 = Job(
#     index=1,
#     time_completion=10,
#     time_limit=15,
#     ret_cost_factor=3,
#     pen_cost_factor=10,
# )
# job_2 = Job(
#     index=2,
#     time_completion=8,
#     time_limit=20,
#     ret_cost_factor=2,
#     pen_cost_factor=22,
# )
# job_3 = Job(
#     index=3,
#     time_completion=6,
#     time_limit=10,
#     ret_cost_factor=5,
#     pen_cost_factor=10,
# )
# job_4 = Job(
#     index=4,
#     time_completion=7,
#     time_limit=30,
#     ret_cost_factor=4,
#     pen_cost_factor=8,
# )
# job_5 = Job(
#     index=5,
#     time_completion=4,
#     time_limit=12,
#     ret_cost_factor=6,
#     pen_cost_factor=15,
# )

# jobstep_1 = JobStep(job_1=job_1, job_2=job_2, visited=True, order=1)
# jobstep_2 = JobStep(job_1=job_2, job_2=job_3, visited=True, order=2)
# jobstep_3 = JobStep(job_1=job_3, job_2=job_4, visited=True, order=3)
# jobstep_4 = JobStep(job_1=job_4, job_2=job_5, visited=True, order=4)
# jobstep_5 = JobStep(job_1=job_5, job_2=job_1, visited=True, order=5)

# chromosome = BinaryChromosome(
#     id=1,
#     gene=[
#         jobstep_1,
#         jobstep_2,
#         jobstep_3,
#         jobstep_4,
#         jobstep_5,
#     ],
# )
# chromosome._get_visited_jobsteps()
# BinaryChromosome._valid_gene(chromosome._get_visited_jobsteps())

# chromosome._select_random_order()
# %%


# %%


class BinaryGeneticAlgorithm:
    def __init__(
        self,
        population: dict[int, BinaryChromosome],
        only_feasable_solutions: bool = True,
    ) -> None:
        self.population: dict[int, BinaryChromosome] = population
        self.new_population: dict[int, BinaryChromosome] = dict()
        self.population_size: int = len(population)

        self.only_feasable_solutions = only_feasable_solutions

    @classmethod
    def from_scenario(
        cls,
        scenario: pd.DataFrame,
        n: int,
        only_feasable_solutions: bool = True,
    ):
        ## n: Número de chromosomas que se quieren crear

        population = {
            i: BinaryChromosome.from_dataframe(scenario=scenario, id=i)
            for i in range(n)
        }

        return cls(
            population=population,
            only_feasable_solutions=only_feasable_solutions,
        )

    # %%

    def _evaluate_population(self):
        self.fitness_values: dict[int, Number] = dict()
        self.cost_values: dict[int, Number] = dict()

        for idx, chromosome in self.population.items():
            # if not self._valid_chromosome(chromosome):
            #     self.fitness_values.update({idx: 0})
            # else:
            self.fitness_values.update(
                {idx: (1 / chromosome._calculate_gene_cost()) * 1000}
            )
            self.cost_values.update({idx: chromosome._calculate_gene_cost()})

    def _select_parents(self) -> list[BinaryChromosome, BinaryChromosome]:
        total_fitness = sum(self.fitness_values.values())

        try:
            self.probabilities = {
                chromosome_id: fitness / total_fitness
                for chromosome_id, fitness in self.fitness_values.items()
            }
        except ZeroDivisionError as ze:
            self.probabilities = {
                chromosome_id: fitness / self.population_size(total_fitness)
                for chromosome_id, fitness in self.fitness_values.items()
            }

        chromosomes = list(self.probabilities.keys())
        weights = list(self.probabilities.values())

        parent_1_id, parent_2_id = random.choices(
            population=chromosomes,
            weights=weights,
            k=2,
        )

        parent_1 = self.population.get(parent_1_id)
        parent_2 = self.population.get(parent_2_id)

        return parent_1, parent_2

    def crossover(
        self,
        parent_1: BinaryChromosome,
        parent_2: BinaryChromosome,
    ) -> tuple[BinaryChromosome, BinaryChromosome]:
        child_1 = BinaryChromosome(
            id=0,
            gene=parent_1.gene[: self.crossover_point]
            + parent_2.gene[self.crossover_point :],
        )
        child_2 = BinaryChromosome(
            id=0,
            gene=parent_2.gene[: self.crossover_point]
            + parent_1.gene[self.crossover_point :],
        )

        return child_1, child_2

    def mutate(self, chromosome: BinaryChromosome) -> BinaryChromosome:
        mutation_index = random.randint(0, len(chromosome.gene) - 1)

        _new_chromosome = deepcopy(chromosome)
        job_step_name = chromosome.gene[mutation_index].name

        _new_chromosome._switch_visited_jobstep(f"{job_step_name}")

        if self.only_feasable_solutions:
            visited_jobsteps = _new_chromosome._get_visited_jobsteps()
            if not _new_chromosome._valid_gene(visited_jobsteps):
                _new_chromosome._switch_visited_jobstep(f"{job_step_name}")

        self.new_population.update({_new_chromosome.id: _new_chromosome})

    # def _valid_chromosome(self, chromosome: BinaryChromosome):
    #     return chromosome._calculate_gene_cost() <= self.max_cost

    def solve(
        self,
        generations: int,
        crossover_point: int,
        crossover_rate: float,
        mutation_rate: float,
    ) -> tuple[BinaryChromosome, float]:
        self.crossover_point = crossover_point

        start = perf_counter()

        for generation in range(1, generations + 1):
            logger.info(f"---- CURRENT GENERATION: {generation}")
            self._evaluate_population()

            logger.debug(f"{self.fitness_values=}")
            logger.debug(f"{self.cost_values=}")

            # Select parents and perform crossover
            self.new_population: dict[int, BinaryChromosome] = dict()
            logger.debug(f"Cromosomas Nueva Generacion: {len(self.new_population)}")
            while len(self.new_population) < self.population_size:
                parent_1, parent_2 = self._select_parents()

                if random.random() <= crossover_rate:
                    child_1, child_2 = self.crossover(
                        parent_1=parent_1,
                        parent_2=parent_2,
                    )
                else:
                    child_1, child_2 = deepcopy(parent_1), deepcopy(parent_2)

                if self.only_feasable_solutions:
                    logger.debug(f"{child_1=}")
                    logger.debug(f"{child_2=}")

                    visited_child_1 = deepcopy(child_1._get_visited_jobsteps())
                    visited_child_2 = deepcopy(child_2._get_visited_jobsteps())

                    if child_1._valid_gene(visited_child_1):
                        child_1.id = len(self.new_population) + 1
                        self.new_population.update({child_1.id: child_1})
                        logger.debug(
                            f"Cromosomas Nueva Generacion: {len(self.new_population)}"
                        )

                        logger.debug("CHILD 1 LIVED")

                        if len(self.new_population) >= self.population_size:
                            break

                    if child_2._valid_gene(visited_child_2):
                        child_2.id = len(self.new_population) + 1
                        self.new_population.update({child_2.id: child_2})
                        logger.debug(
                            f"Cromosomas Nueva Generacion: {len(self.new_population)}"
                        )

                        logger.debug("CHILD 2 LIVED")

                        if len(self.new_population) >= self.population_size:
                            break
                else:
                    child_1.id = len(self.new_population) + 1
                    self.new_population.update({child_1.id: child_1})
                    logger.debug(
                        f"Cromosomas Nueva Generacion: {len(self.new_population)}"
                    )

                    if len(self.new_population) >= self.population_size:
                        break

                    child_2.id = len(self.new_population) + 1
                    self.new_population.update({child_2.id: child_2})
                    logger.debug(
                        f"Cromosomas Nueva Generacion: {len(self.new_population)}"
                    )

                    if len(self.new_population) >= self.population_size:
                        break
            # Apply mutation
            for _, chromosome in self.new_population.items():
                if random.random() < mutation_rate:
                    self.mutate(chromosome)

            if self.only_feasable_solutions:
                for id_, chromosome in self.new_population.items():
                    visited_chromosome = deepcopy(chromosome._get_visited_jobsteps())

                    assert chromosome._valid_gene(
                        visited_chromosome
                    ), f"Invalid Chromosome in New Population.\nInvalid Chromosome ID : {id_}\nInvalid Chromosome : {chromosome}\nNew Population: {self.new_population}"

            self.population = deepcopy(self.new_population)

        self._evaluate_population()
        logger.debug(f"Final Generation Fitness: {self.fitness_values}")
        logger.debug(f"Final Generation Costs: {self.cost_values}")

        # Return the best solution found
        best_solution_id: int = max(
            self.fitness_values,
            key=self.fitness_values.get,
        )

        self.best_solution = self.population[best_solution_id]

        end = perf_counter()
        exec_time = end - start

        self.print_solution()

        return self.best_solution, exec_time

    def print_solution(self):
        solution_path = self.best_solution._get_visited_jobsteps()

        print("\nSOLUTION:\n------")
        for i, node in enumerate(solution_path, start=1):
            if i != len(solution_path):
                print(f"{node.name} --> ", end="")
            else:
                print(node.name)

        print(f"Costo Total: {self.best_solution._calculate_gene_cost()}\n")
