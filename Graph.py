import matplotlib.colors as mcolors
import random
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


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

    def visualize(self, ants_number, iteration_number):
        G = nx.DiGraph()
        for source, edges in self.graph.items():
            for edge in edges:
                G.add_edge(source, edge.destination,
                           weight=edge.weight, pheromone=edge.pheromone)

        pos = nx.spring_layout(G)

        # Define colormap
        colormap = plt.cm.Reds

        # Normalize edge pheromones to map to colors along the colormap
        norm = mcolors.Normalize(vmin=min(edge.pheromone for source, edges in self.graph.items() for edge in edges),
                                 vmax=max(edge.pheromone for source, edges in self.graph.items() for edge in edges))

        # Draw nodes
        nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue",
                font_size=15, font_weight="bold", arrowsize=20)

        # Draw edges with edge colors based on normalized pheromones
        for source, destination, edge_data in G.edges(data=True):
            nx.draw_networkx_edges(G, pos, edgelist=[(
                source, destination)], width=2, edge_color=colormap(norm(edge_data['pheromone'])))

        # Add edge labels
        edge_labels = {(source, destination): edge_data['weight']
                       for source, destination, edge_data in G.edges(data=True)}
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=edge_labels, font_color='black')

        # Create colorbar
        sm = plt.cm.ScalarMappable(cmap=colormap, norm=norm)
        sm.set_array([])
        # Specify the axes for the colorbar
        cbar = plt.colorbar(sm, ax=plt.gca(), label='Edge Pheromone')

        # Add text for ants number and iteration number
        plt.text(
            0.05, 0.05, f'Ants Number: {ants_number}', transform=plt.gca().transAxes)
        plt.text(
            0.05, 0.1, f'Iteration Number: {iteration_number}', transform=plt.gca().transAxes)

        plt.title("Graph Visualization")
        plt.show()

    def print_graph(self, num_of_cities):
        for source in range(1, num_of_cities + 1):
            for edge in self.graph[source]:
                print(source, edge.destination, edge.weight)


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


def hard_coded_graphs():
    graph = Graph()
    for i in range(20):
        s = input().split(' ')
        node = int(s[0])
        destination = int(s[1])
        weight = int(s[2])
        graph.add_edge(node, destination, weight)
        # graph.add_edge(destination, node, weight)

    return graph
