import random

import numpy as np
from dataclasses import dataclass
from numbers import Number
from time import perf_counter, sleep
from copy import deepcopy

from utils._logging import logger


@dataclass
class Container:
    name: str
    benefit: Number
    cost: Number
    is_used: bool


class BinaryChromosome:
    def __init__(self, id: int, gene: list[Container]):
        self.id = id
        self.gene = gene

        self.cost = self._calculate_gene_cost()
        self.benefit = self._calculate_gene_benefit()

    def _calculate_gene_cost(self):
        return sum(container.cost for container in self.gene if container.is_used)

    def _calculate_gene_benefit(self):
        return sum(container.benefit for container in self.gene if container.is_used)

    def _get_used_containers(self) -> list[Container]:
        return [container for container in self.gene if container.is_used]

    def _switch_used_container(self, container_name: str):
        for container in self.gene:
            if container.name == container_name:
                container.is_used = bool(True - container.is_used)
                break

    def print_gene(self):
        for container in self.gene:
            logger.info(container)

    def __repr__(self) -> str:
        return f"""
{"ID".ljust(7)}: {self.id}
{"Gene".ljust(7)}: {self.gene}
{"Benefit".ljust(7)}: {self._calculate_gene_benefit()}
{"Cost".ljust(7)}: {self._calculate_gene_cost()}"""


# TODO Añadir criterio de infactibilidad en algun lado
class BinaryGeneticAlgorithm:
    def __init__(
        self,
        population: dict[int, BinaryChromosome],
        max_cost: Number,
        only_feasable_solutions: bool = True,
    ) -> None:
        self.population: dict[int, BinaryChromosome] = population
        self.new_population: dict[int, BinaryChromosome] = dict()
        self.population_size: int = len(population)
        self.max_cost: Number = max_cost

        self.only_feasable_solutions = only_feasable_solutions

    @classmethod
    def from_random(
        cls,
        benefits: list[Number],
        costs: list[Number],
        max_cost: Number,
        only_feasable_solutions: bool = True,
    ):
        chromosomes = cls._create_random_chromosomes(
            benefits_=benefits,
            costs_=costs,
            max_cost_=max_cost,
            only_feasable_solutions_=only_feasable_solutions,
        )

        return cls(
            population=chromosomes,
            max_cost=max_cost,
            only_feasable_solutions=only_feasable_solutions,
        )

    @staticmethod
    def _create_random_chromosomes(
        benefits_: list[Number],
        costs_: list[Number],
        max_cost_: Number,
        only_feasable_solutions_: bool = True,
    ) -> list[BinaryChromosome]:
        assert len(benefits_) == len(
            costs_
        ), f"The length of the vectors of benefits and costs should be the same length. Was given benefits: {len(benefits_)} and costs: {len(costs_)}"

        chromosomes = dict()

        for i, _ in enumerate(benefits_, start=1):
            containers = __class__._create_random_containers(
                benefits_=benefits_, costs_=costs_
            )

            chromosome = BinaryChromosome(id=i, gene=containers)

            if only_feasable_solutions_:
                while not chromosome.cost <= max_cost_:
                    containers = __class__._create_random_containers(
                        benefits_=benefits_, costs_=costs_
                    )

                    chromosome = BinaryChromosome(id=i, gene=containers)

            chromosomes.update({i: BinaryChromosome(id=i, gene=containers)})

        return chromosomes

    @staticmethod
    def _create_random_containers(
        benefits_: list[Number],
        costs_: list[Number],
    ):
        containers = list()
        for i, (benefit, cost) in enumerate(zip(benefits_, costs_), start=1):
            containers.append(
                Container(
                    name=f"c{i}",
                    benefit=benefit,
                    cost=cost,
                    is_used=random.choice([True, False]),
                )
            )
        return containers

    def _evaluate_population(self):
        self.fitness_values: dict[int, Number] = dict()
        self.cost_values: dict[int, Number] = dict()

        for idx, chromosome in self.population.items():
            if not self._valid_chromosome(chromosome):
                self.fitness_values.update({idx: 0})
            else:
                self.fitness_values.update({idx: chromosome._calculate_gene_benefit()})

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

        _new_chromosome._switch_used_container(f"c{mutation_index}")

        if self.only_feasable_solutions:
            if not self._valid_chromosome(_new_chromosome):
                _new_chromosome._switch_used_container(f"c{mutation_index}")

        self.new_population.update({_new_chromosome.id: _new_chromosome})

    def _valid_chromosome(self, chromosome: BinaryChromosome):
        return chromosome._calculate_gene_cost() <= self.max_cost

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
            self.new_population = dict()
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
                    if self._valid_chromosome(child_1):
                        child_1.id = len(self.new_population) + 1
                        self.new_population.update({child_1.id: child_1})
                        logger.debug(
                            f"Cromosomas Nueva Generacion: {len(self.new_population)}"
                        )

                        if len(self.new_population) >= self.population_size:
                            break

                    if self._valid_chromosome(child_2):
                        child_2.id = len(self.new_population) + 1
                        self.new_population.update({child_2.id: child_2})
                        logger.debug(
                            f"Cromosomas Nueva Generacion: {len(self.new_population)}"
                        )

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
                    assert self._valid_chromosome(
                        chromosome
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
        logger.debug(f"{best_solution_id=}")

        end = perf_counter()
        exec_time = end - start

        self.print_solution()

        return self.best_solution, exec_time

    def print_solution(self):
        solution_path = [
            container.name for container in self.best_solution.gene if container.is_used
        ]

        print("\nSOLUTION:\n------")
        for i, node in enumerate(solution_path, start=1):
            if i != len(solution_path):
                print(f"{node} --> ", end="")
            else:
                print(node)

        print(f"\nFunción Objetivo: {self.best_solution._calculate_gene_benefit()}")
        print(f"Costo Total: {self.best_solution._calculate_gene_cost()}\n")
