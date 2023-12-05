import numpy as np
import pandas as pd


class AntColony:
    def __init__(self, distance_matrix, n_ants, decay=0.1, alpha=1, beta=2):
        self.distance_matrix = distance_matrix
        self.pheromone_matrix = pd.DataFrame(
            np.ones_like(distance_matrix) / len(distance_matrix),
            index=distance_matrix.index,
            columns=distance_matrix.columns,
        )
        self.all_paths = distance_matrix.index
        self.n_ants = n_ants
        self.decay = decay
        self.alpha = alpha
        self.beta = beta

    def run(self, n_iterations):
        best_path = None
        best_distance = float("inf")

        for _ in range(n_iterations):
            all_paths = self.generate_paths()
            self.update_pheromones(all_paths)

            if min(all_paths.values()) < best_distance:
                best_path = min(all_paths, key=all_paths.get)
                best_distance = all_paths[best_path]

        return best_path, best_distance

    def generate_paths(self):
        all_paths = {}
        for ant in range(self.n_ants):
            path = self.generate_path()
            distance = self.calculate_distance(path)
            all_paths[tuple(path)] = distance

        return all_paths

    def generate_path(self):
        paths = np.zeros((self.n_ants, len(self.all_paths)), dtype=int)

        for ant in range(self.n_ants):
            path = [np.random.choice(self.all_paths)]
            for _ in range(len(self.all_paths) - 1):
                path = self.move_to_next_city(path[-1], path)

            paths[ant] = path

        return paths

    def move_to_next_city(self, current_city, path):
        pheromones = np.copy(self.pheromone_matrix.loc[current_city].values)
        pheromones[path] = 0

        probabilities = (pheromones**self.alpha) * (
            (1 / self.distance_matrix.loc[current_city]) ** self.beta
        )
        probabilities /= probabilities.sum()

        probabilities = probabilities.fillna(0)

        next_city = np.random.choice(self.all_paths, p=probabilities)
        path.append(next_city)

        return path

    def calculate_distance(self, path):
        distance = 0
        for i in range(len(path) - 1):
            distance += self.distance_matrix.loc[path[i], path[i + 1]]
        distance += self.distance_matrix.loc[
            path[-1], path[0]
        ]  # Return to the starting city
        return distance

    def update_pheromones(self, all_paths):
        self.pheromone_matrix *= 1 - self.decay

        for path, distance in all_paths.items():
            for i in range(len(path) - 1):
                self.pheromone_matrix.loc[path[i], path[i + 1]] += 1 / distance
            self.pheromone_matrix.loc[path[-1], path[0]] += 1 / distance


# # Example Usage:
# # Assuming 'distance_matrix' is your Pandas DataFrame
# distance_matrix = pd.DataFrame(
#     {
#         "City1": {"City1": 0, "City2": 2, "City3": 3, "City4": 5, "City5": 6},
#         "City2": {"City1": 2, "City2": 0, "City3": 1, "City4": 3, "City5": 4},
#         "City3": {"City1": 3, "City2": 1, "City3": 0, "City4": 2, "City5": 5},
#         "City4": {"City1": 5, "City2": 3, "City3": 2, "City4": 0, "City5": 1},
#         "City5": {"City1": 6, "City2": 4, "City3": 5, "City4": 1, "City5": 0},
#     }
# )

# ant_colony = AntColony(distance_matrix, n_ants=10, decay=0.1, alpha=1, beta=2)
# best_path, best_distance = ant_colony.run(n_iterations=100)

# print("Best Path:", best_path)
# print("Best Distance:", best_distance)
