import networkx as nx
import numpy as np
import galois as gl
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
        self.dim = max(len(simplex) for simplex in self.simplices) - 1
        self.field = gl.GF(2)

    def construct_graph(self):
        graph = nx.Graph()
        graph.add_nodes_from(self.vertex_names)
        for i, j in combinations(self.vertex_names, 2):
            if self.metric(self.vertices[i], self.vertices[j]) <= 2*self.radius:
                graph.add_edge(i, j)
        return graph

    def get_simplices(self):
        cliques = list(nx.find_cliques(self.graph))
        simplices = [list(sorted(clique)) for clique in cliques]
        return sorted(simplices, key=lambda simplex: (len(simplex), simplex[0]))

    def get_p_simplices(self, dim):
        if dim == 0:
            return [list(face) for face in self.vertex_names]
        elif dim < 0 or dim > self.dim:
            return [[]]
        else:
            higher_simplices = [simplex for simplex in self.simplices if len(simplex) >= dim + 1]
            faces = []
            for simplex in higher_simplices:
                for face in combinations(simplex, dim + 1):
                    faces.append(list(face))
            return sorted(faces, key=lambda face: face[0])
    
    def get_all_simplices(self):
        simplices = [tuple(vertex) for vertex in self.vertex_names]

        for simplex in self.simplices:
            for dim in range(1, len(simplex)):
                for face in combinations(simplex, dim+1):
                    simplices.append(face)
        
        simplices = list(set(simplices))
        simplices = [list(simplex) for simplex in simplices]
        return sorted(simplices, key=lambda simplex: (len(simplex), simplex[0]))
    
    def get_p_boundary_matrix(self, dim):
        p_simplices = self.get_p_simplices(dim)
        faces = self.get_p_simplices(dim - 1)

        if p_simplices == [[]] and faces == [[]]:
            boundary_matrix = self.field([[0]])
            return boundary_matrix

        elif p_simplices == [[]]:
            boundary_matrix = self.field(np.zeros(len(faces), dtype=int))
            boundary_matrix = boundary_matrix.reshape([len(faces), 1])
            return boundary_matrix

        elif faces == [[]]:
            boundary_matrix = self.field(np.zeros(len(p_simplices), dtype=int))
            boundary_matrix = boundary_matrix.reshape([1, len(p_simplices)])
            return boundary_matrix

        boundary_matrix = []
        
        for simplex in p_simplices:
            boundary = []
            for face in faces:
                if set(face).issubset(set(simplex)):
                    boundary.append(1)
                else:
                    boundary.append(0)
            boundary_matrix.append(boundary)
        
        return np.transpose(self.field(boundary_matrix))
    
    def get_p_betti(self, dim):
        p_boundary_matrix = self.get_p_boundary_matrix(dim)
        p1_boundary_matrix = self.get_p_boundary_matrix(dim+1)

        zero = self.field([[0]])
        if np.array_equal(p_boundary_matrix, zero) and np.array_equal(p1_boundary_matrix, zero):
            return 0

        return p_boundary_matrix.shape[1] - np.linalg.matrix_rank(p_boundary_matrix) - np.linalg.matrix_rank(p1_boundary_matrix)

    def get_betti(self):
        return [self.get_p_betti(p) for p in range(self.dim+1)]