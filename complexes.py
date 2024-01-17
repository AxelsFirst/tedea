import networkx as nx
import numpy as np
import galois as gl
from itertools import combinations
from metrics import euclidean_metric


class VietorisRipsComplex:
    """
    Representation of a Vietoris-Rips abstract simplicial complex.

    Parameters
    ----------
    vertices: list of list of float
              Coordinates of vertices.
    radius: float
    vertex_names: list of str or None, default=None
                  Optional labels of vertices.
    metric: function
            Metric used for getting distances between vertices, by default Euclidean metric.

    Attributes
    ----------
    vertex_names: list of str
                  Labels of vertices, if parsed None then indexes of vertices.
    vertices: dict
              Translation of names of vertices to coordinates of vertices.
    radius: float
    graph: Graph
           Graph of a simplicial complex.
    simplices: list of list of str
               Unique simplices of a complex, that are not faces of other simplices.
    dim: int
         Dimension of simplicial complex.
    field: FieldArrayMeta
           Z/2Z field of coefficients of matrices.
    """

    def __init__(self, vertices, radius, vertex_names=None, metric=euclidean_metric):
        """
        Assigns complex parameters using parsed parameters and initiates calculations.

        Arguments
        ----------
        vertices: list of list of float
                Coordinates of vertices.
        radius: float
        vertex_names: list of str or None, default=None
                    Optional labels of vertices.
        metric: function
                Metric used for getting distances between vertices, by default Euclidean metric.
        """

        self.vertex_names = vertex_names or [str(i) for i in range(len(self.vertices))]
        self.vertices = dict(zip(self.vertex_names, vertices))
        self.radius = radius
        self.metric = metric
        self.graph = self.construct_graph()
        self.simplices = self.get_simplices()
        self.dim = max(len(simplex) for simplex in self.simplices) - 1
        self.field = gl.GF(2)

    def construct_graph(self):
        """
        Contruct a graph of a Vietoris-Rips simplicial complex, adds an edge between two
        distinct vertices if the distance is smaller than the diameter, ie radius times two.

        Returns
        -------
        graph: Graph
               Graph of a simplicial complex.
        """

        graph = nx.Graph()
        graph.add_nodes_from(self.vertex_names)
        for i, j in combinations(self.vertex_names, 2):
            if self.metric(self.vertices[i], self.vertices[j]) <= 2*self.radius:
                graph.add_edge(i, j)
        return graph

    def get_simplices(self):
        """
        Finds unique simplices of a complex, that are not faces of other simplices.

        Returns
        -------
        simplices: list of list of str
                   Unique simplices of a complex, that are not faces of other simplices.
        """

        cliques = list(nx.find_cliques(self.graph))
        simplices = [list(sorted(clique)) for clique in cliques]
        return sorted(simplices, key=lambda simplex: (len(simplex), simplex[0]))

    def get_p_simplices(self, dim):
        """
        Finds all p-simplices of a complex, i.e. simplices of p-th dimension.

        Arguments
        ---------
        dim: int
             Dimension p of a p-simplex.
        
        Returns
        -------
        simplices: list of list of str
                   All p-simplices of a simplicial complex, i.e. simplices of p-th dimension.
        """

        if dim == 0:
            return [list(face) for face in self.vertex_names]
        elif dim < 0 or dim > self.dim:
            return [[]]
        else:
            higher_simplices = [simplex for simplex in self.simplices if len(simplex) >= dim + 1]
            faces = []
            for simplex in higher_simplices:
                for face in combinations(simplex, dim + 1):
                    faces.append(face)
            unique_faces = set(tuple(faces))
            faces = [[vertex for vertex in face] for face in unique_faces]
            return sorted(faces, key=lambda face: face[0])
    
    def get_all_simplices(self):
        """
        Finds all simplices of a complex.
        
        Returns
        -------
        simplices: list of list of str
                   All simplices of a simplicial complex.
        """

        simplices = [tuple(vertex) for vertex in self.vertex_names]

        for simplex in self.simplices:
            for dim in range(1, len(simplex)):
                for face in combinations(simplex, dim+1):
                    simplices.append(face)
        
        simplices = list(set(simplices))
        simplices = [list(simplex) for simplex in simplices]
        return sorted(simplices, key=lambda simplex: (len(simplex), simplex[0]))
    
    def get_p_boundary_matrix(self, dim):
        """
        Creates a p-th boundary matrix, i.e. a matrix of a p-th boundary operator.
        
        Arguments
        ---------
        dim: int
             Dimension p of a p-th boundary operator.
        
        Returns
        -------
        boundary_matrix: GF(2)
                         2D array, i.e. matrix with coefficients over Z/2Z.
        """

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
        """
        Calculates p-th Betti number, i.e. dimension of a p-th homology group of a simplicial complex.

        Arguments
        ---------
        dim: int
             Dimension p of a p-th homology group.
        
        Returns
        -------
        betti: int
               p-th Betti number.
        """

        p_boundary_matrix = self.get_p_boundary_matrix(dim)
        p1_boundary_matrix = self.get_p_boundary_matrix(dim+1)

        zero = self.field([[0]])
        p_zero = np.array_equal(p_boundary_matrix, zero)
        p1_zero = np.array_equal(p1_boundary_matrix, zero)
        if p_zero and p1_zero:
            return 0

        col_num = p_boundary_matrix.shape[1]
        p_rank = np.linalg.matrix_rank(p_boundary_matrix)
        p1_rank = np.linalg.matrix_rank(p1_boundary_matrix)
        return col_num - p_rank - p1_rank

    def get_betti(self):
        """
        Returns all relevant Betti numbers of a simplicial complex, that is up to k-th one, 
        where k is dimension of a simplicial complex.

        Returns
        -------
        betti_numbers: list of int
                       All relevant Betti numbers of a simplicial complex.
        """

        return [self.get_p_betti(p) for p in range(self.dim+1)]