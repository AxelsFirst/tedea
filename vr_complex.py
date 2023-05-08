import networkx as nx


class Vietoris_Rips_Complex:
    """

    Representation of the Vietoris Rips Complex

    """

    def __init__(self, points, epsilon, metric) -> None:
        self.points = points
        self.epsilon = epsilon
        self.metric = metric

        self._create_simplicial_complex()

    def _create_complex(self) -> None:
        self.graph = nx.Graph()
        self._add_points

    def _add_points_complex(self) -> None:
        self.graph.add_nodes_from(self.points)
