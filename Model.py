import Graph
import random
import bisect
from sortedcontainers import SortedSet

NUM_OF_CITIES = 10
NUMS_OF_ANTS = [1, 5, 10, 20]
NUM_OF_ITERATOINS = 50
ALPHA = 2
BETA = 3
Q = 100
VAPORIZING_RATE = 0.1
WEIGHT_MULTIPLIER = 10


class Ant:
    def __init__(self, id):
        self.id = id
        self.path = []
        self.nodes = []
        self.total_weight = 0


ants = []


def run():
    graph = Graph.generate_random_graph(NUM_OF_CITIES, 5)
    for i in NUMS_OF_ANTS:
        temp = graph
        train(i, temp)
        graph.visualize()
    opt_sol(graph)


def train(num_of_ants, graph):

    ants.clear()
    for i in range(1, num_of_ants + 1):
        ants.append(Ant(i))

    for _ in range(NUM_OF_ITERATOINS):
        for ant in ants:
            destination = random.randint(1, NUM_OF_CITIES)
            ant.nodes.append(destination)
            traverse(destination, ant, graph, None, destination)

            # Adding pheromone
            for node, edges in graph.graph.items():
                for edge in edges:
                    if edge in ant.path:
                        if ant.total_weight == 0:
                            ant.total_weight = 10000
                        edge.to_be_added_pheromone += Q/(ant.total_weight ** 2)

            if len(ant.path) == NUM_OF_CITIES:
                print("Ant ID:", ant.id)
                print(destination)
                for i in ant.path:
                    print(i.destination)
                print("Total weight: ", ant.total_weight)
            ant.path.clear()
            ant.nodes.clear()
            ant.total_weight = 0
        for node, edges in graph.graph.items():
            for edge in edges:
                edge.pheromone = (
                    edge.pheromone * (1-VAPORIZING_RATE)) + edge.to_be_added_pheromone
                edge.to_be_added_pheromone = 0


def traverse(node, ant, graph, edge, dest):
    if len(ant.path) >= NUM_OF_CITIES:
        return

    total_probability = 0
    probabilities = []
    for v in graph.get_neighbors(node):
        if v.destination not in ant.nodes:
            probability = (v.pheromone**ALPHA) * \
                ((WEIGHT_MULTIPLIER / v.weight)**BETA)
            probabilities.append((probability, v))
            total_probability += probability
        elif v.destination == dest and len(ant.nodes) == NUM_OF_CITIES:
            probability = (v.pheromone**ALPHA) * \
                ((WEIGHT_MULTIPLIER / v.weight)**BETA)
            probabilities.append((probability, v))
            total_probability += probability
    if total_probability == 0:
        return
    random_choice = random.random()
    cumulative_sum = 0
    cumulative_sums = []
    for pair in probabilities:
        cumulative_sum += pair[0]
        cumulative_sums.append(cumulative_sum/total_probability)

    chosen_index = bisect.bisect_left(cumulative_sums, random_choice)
    chosen_node = probabilities[chosen_index][1].destination
    ant.total_weight += probabilities[chosen_index][1].weight

    for v in graph.get_neighbors(node):
        if v == probabilities[chosen_index][1]:
            ant.path.append(v)
            ant.nodes.append(v.destination)
            traverse(chosen_node, ant, graph, v, dest)


optimal_weight = 100000000
visited = {}
VIS = 0
for i in range(1, NUM_OF_CITIES + 1):
    visited[i] = False


def dfs(node, graph, weight, path, dest, optimal_path):
    global optimal_weight, visited, VIS

    visited[node] = True
    VIS += 1

    for v in graph.get_neighbors(node):
        if not visited[v.destination]:
            path.append(v.destination)
            dfs(v.destination, graph, weight +
                v.weight, path, dest, optimal_path)
            path.pop()
        elif v.destination == dest and VIS == NUM_OF_CITIES:
            if weight < optimal_weight:
                path.append(dest)
                optimal_path = path
                optimal_weight = weight
                path.pop()
    VIS -= 1
    visited[node] = False


def opt_sol(graph):
    global optimal_weight
    optimal_path = []
    for i in range(1, NUM_OF_CITIES):
        dfs(i, graph, 0, [], i, optimal_path)
    print("The optimal path:")
    print(optimal_path)
    print(optimal_weight)
