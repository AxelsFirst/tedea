import networkx as nx
import numpy as np
from itertools import combinations

def euclidean_metric(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))

class VietorisRipsComplex:
    def __init__(self, vertices, radius, vertex_names=None, metric=euclidean_metric):
        self.vertex_names = vertex_names or [str(i) for i in range(len(self.vertices))]
        self.vertices = dict(zip(self.vertex_names, vertices))
        self.radius = radius
        self.metric = metric
        self.graph = self.construct_graph()
        self.simplices = self.get_simplices()

    def construct_graph(self):
        graph = nx.Graph()
        graph.add_nodes_from(self.vertex_names)
        for i, j in combinations(self.vertex_names, 2):
            if self.metric(self.vertices[i], self.vertices[j]) <= self.radius:
                graph.add_edge(i, j)
        return graph

    def get_simplices(self):
        cliques = list(nx.find_cliques(self.graph))
        simplices = sorted([list(sorted(clique)) for clique in cliques])
        return simplices

    def get_p_simplices(self, dim):
        if dim == 0:
            return [list(face) for face in self.vertex_names]
        else:
            length_of_simplices = dim + 1
            higher_simplices = [simplex for simplex in self.simplices if len(simplex) >= length_of_simplices]
            faces = []
            for simplex in higher_simplices:
                for face in combinations(simplex, length_of_simplices):
                    faces.append(list(face))
            return sorted(faces)
    
    def boundary_matrix(self, dim):
        boundary_matrix = []
        p_simplices = self.get_p_simplices(dim)
        faces = self.get_p_simplices(dim - 1)
        
        for simplex in p_simplices:
            boundary = []
            for face in faces:
                if set(face).issubset(set(simplex)):
                    boundary.append(1)
                else:
                    boundary.append(0)
            boundary_matrix.append(boundary)
        
        return np.transpose(np.array(boundary_matrix))