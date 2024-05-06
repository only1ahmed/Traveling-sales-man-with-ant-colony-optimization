import random
import networkx as nx
import matplotlib.pyplot as plt


class Edge:
    def __init__(self, destination, weight):
        self.destination = destination
        self.weight = weight
        self.pheromone = 1
        self.to_be_added_pheromone = 0

    def __str__(self):
        return f"(destination: {self.destination}, weight: {self.weight}, pheromone: {self.pheromone})"


class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, source, destination, weight):
        if source not in self.graph:
            self.graph[source] = []
        self.graph[source].append(Edge(destination, weight))

    def get_neighbors(self, node):
        return self.graph.get(node, [])

    def __str__(self):
        return str(self.graph)

    def visualize(self):
        G = nx.DiGraph()
        for source, edges in self.graph.items():
            for edge in edges:
                G.add_edge(source, edge.destination, weight=edge.weight)

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue",
                font_size=15, font_weight="bold", arrowsize=20)
        edge_labels = {(source, destination): edge_data['weight']
                       for source, destination, edge_data in G.edges(data=True)}

        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=edge_labels, font_color='red')
        plt.title("Graph Visualization")
        plt.show()


def generate_random_graph(num_nodes, num_of_edges):
    graph = Graph()
    for node in range(1, num_nodes + 1):
        nums = []
        for i in range(1, num_nodes + 1):
            if i == node:
                continue
            nums.append(i)
        for i in range(1, num_of_edges + 1):
            rnd = random.randint(0, len(nums) - 1)
            destination = nums[rnd]
            weight = random.randint(3, 50)
            graph.add_edge(node, destination, weight)
            nums.pop(rnd)
    return graph
