import networkx as nx
import numpy as np
from itertools import combinations

def euclidean_metric(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

class VietorisRipsComplex:
    def __init__(self, points, radius, point_names=None, metric=euclidean_metric):
        self.point_names = point_names or [str(i) for i in range(len(self.points))]
        self.points = dict(zip(self.point_names, points))
        self.radius = radius
        self.metric = metric
        self.graph = self.construct_graph()
        self.simplices = self.find_simplices()

    def construct_graph(self):
        graph = nx.Graph()
        graph.add_nodes_from(self.point_names)
        for i, j in combinations(self.point_names, 2):
            if self.metric(self.points[i], self.points[j]) <= self.radius:
                graph.add_edge(i, j)
        return graph

    def find_simplices(self):
        cliques = list(nx.find_cliques(self.graph))
        simplices = [tuple(sorted(clique)) for clique in cliques]
        return simplices

    def get_faces(self, dimension):
        if dimension == 0:
            return self.point_names
        else:
            length_of_simplices = dimension + 1
            higher_simplices = [simplex for simplex in self.simplices if len(simplex) >= length_of_simplices]
            faces = []
            for simplex in higher_simplices:
                for face in combinations(simplex, length_of_simplices):
                    faces.append(tuple(face))
            return faces