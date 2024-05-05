class Edge:
    def __init__(self, destination, weight):
        self.destination = destination
        self.weight = weight
        self.pheromone = 0  # Initial pheromone level

    def __str__(self):
        return f"(destination: {self.destination}, weight: {self.weight}, pheromone: {self.pheromone})"


class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, source, destination, weight):
        if source not in self.graph:
            self.graph[source] = []
        if destination not in self.graph:
            self.graph[destination] = []
        self.graph[source].append(Edge(destination, weight))
        self.graph[destination].append(Edge(source, weight))

    def get_neighbors(self, node):
        return self.graph.get(node, [])

    def __str__(self):
        return str(self.graph)


def generate_random_graph(num_nodes, num_edges_per_node):
    graph = Graph()
    for node in range(1, num_nodes + 1):
        for _ in range(num_edges_per_node):
            destination = random.randint(1, num_nodes)
            weight = random.randint(1, 100)
            graph.add_edge(node, destination, weight)
    return graph
