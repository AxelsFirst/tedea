import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon
from matplotlib.collections import PatchCollection
import networkx as nx
import random
import numpy as np
from metrics import *

def plot_2d_complex(complex,
                    fig=None,
                    ax=None,
                    show_plot=True,
                    fig_width=5,
                    fig_height=5,
                    fig_dpi=150,
                    with_labels=False,
                    font_size=8,
                    vertex_size=150,
                    vertex_interior_color='#fff',
                    vertex_border_color='#000',
                    edge_color='#000',
                    save_as_file=False,
                    file_directory='',
                    file_name='plot_of_complex',
                    file_extension='png',
                    draw_balls=False,
                    metric=euclidean_metric,
                    ball_alpha=0.2,
                    ball_color=None,
                    draw_simplices=True,
                    simplex_alpha=0.2,
                    simplex_color=None,
                    return_fig=True):
    """
    Generates and shows a matplotlib figure of a 2D plot of a simplicial complex.

    Arguments
    ---------
    fig: figure or None, default=None
         Matplotlib figure.
    ax: axis or None, default=None
        Axis of matplotlib figure.
    show_plot: bool, default=True
               If True shows the plot.
    fig_width: float, default=5
               Width of a matplotlib figure.
    fig_height: float, default=5
                Height of a matplotlib figure.
    fig_dpi: float, default=150
             DPI of a matplotlib figure.
    with_labels: bool, default=False
                 If True then labels are placed on vertices.
    font_size: int, default=8
               Font size of labels of vertices.
    vertex_size: float, default=150
                 Size of circles representing vertices.
    vertex_interior_color: str or list of float, default='#fff'
                           Interior color of circles.
    vertex_border_color: str or list of float, default='#000'
                         Border color of circles.
    edge_color: str or list of float, default='#000'
                Color of edges of a simplicial complex.
    save_as_file: bool, default=False
                  If True then plot is saved as a file instead of being shown.
    file_directory: str, default=''
                    Plot file directory excluding file name and extension.
    file_name: str, default='plot_of_complex'
               Plot file name.
    file_extension: str, default='png'
                    Plot file extension, for list of supported extensions 
                    refer to matplotlib documentation.
    draw_balls: bool, default=False
                If True then draws balls of radius of a simplicial complex.
    metric: function, default=euclidean_metric
            Metric used to measure distance from center of balls.
    ball_alpha: float, default=0.2
                Value corresponding to transparency of balls.
    ball_color: None or float, default=None
                Color of balls. If None then color is randomized.
    draw_simplices: bool, default=True
                    If True then draws a plot of a simplicial complex by highlighting simplices.
                    If False then draws graph of a simplicial complex by omitting simplices.
    simplex_alpha: float, default=0.2
                   Value corresponding to transparency of simplices.
    simplex_color: None or float or dict of int into float
                   Color of simplices. If None then colors of simplices are randomized 
                   and grouped into respective dimensions. If float then all simplices 
                   share same color. If dict of dimensions p of p-simplices onto colors 
                   then simplices have color assigned by dict.
    """
    if fig is None or ax is None:
        fig, ax = plt.subplots()
    fig.set_figheight(fig_width)
    fig.set_figwidth(fig_height)
    fig.set_dpi(fig_dpi)
    ax.axis('equal')

    nx.draw(G=complex.graph,
            ax=ax,
            pos=complex.vertices,
            with_labels=with_labels,
            font_size=font_size,
            node_size=vertex_size,
            node_color=vertex_interior_color,
            edge_color=vertex_border_color,
            edgecolors=edge_color)
    
    if draw_balls:
        if metric == euclidean_metric:
            for vertex in complex.vertices.values():
                if ball_color is None:
                    color = [random.random() for _ in range(3)]
                else:
                    color = ball_color

                ball = Circle(vertex,
                              radius=complex.radius,
                              alpha=ball_alpha,
                              edgecolor=None,
                              facecolor=color,
                              zorder=-1)

                ax.add_artist(ball)

        if metric == manhattan_metric:
            for vertex in complex.vertices.values():
                if ball_color is None:
                    color = [random.random() for _ in range(3)]
                else:
                    color = ball_color

                ball_anchor = np.array(vertex) - np.array([0, complex.radius])
                edge_length = euclidean_metric([-complex.radius,0], [0,-complex.radius])
                ball = Rectangle(ball_anchor, 
                                 edge_length, 
                                 edge_length,
                                 angle=45,
                                 alpha=ball_alpha,
                                 edgecolor=None,
                                 facecolor=color,
                                 zorder=-1)

                ax.add_artist(ball)

        if metric == maximum_metric:
            for vertex in complex.vertices.values():
                if ball_color is None:
                    color = [random.random() for _ in range(3)]
                else:
                    color = ball_color

                ball_anchor = np.array(vertex) - np.array([complex.radius, complex.radius])
                ball = Rectangle(ball_anchor, 
                                 2*complex.radius, 
                                 2*complex.radius,
                                 alpha=ball_alpha,
                                 edgecolor=None,
                                 facecolor=color,
                                 zorder=-1)

                ax.add_artist(ball)
    
    if draw_simplices:
        simplices = [simplex for simplex in complex.get_all_simplices() if len(simplex) > 2]

        for dim in range(2, complex.dim+1):
            p_simplices = [simplex for simplex in simplices if len(simplex) == dim+1]
            polygons = []

            for simplex in p_simplices:
                vertices = [complex.vertices[vertex] for vertex in simplex]
                polygons.append(Polygon(vertices, closed=True, ))
            
            patches = PatchCollection(polygons)

            if simplex_color is None:
                patches.set_color([random.random() for _ in range(3)])
            elif isinstance(simplex_color, dict):
                patches.set_color(simplex_color[dim])
            else:
                patches.set_color(simplex_color)
            
            patches.set_zorder(-1)
            patches.set_alpha(simplex_alpha)
            
            ax.add_collection(patches)

    plt.tight_layout()

    if save_as_file:
        plt.savefig(f'{file_directory}{file_name}.{file_extension}')
    if show_plot:
        plt.show()
    if return_fig:
        return fig, ax
    
def plot_3d_complex(complex,
                    fig=None,
                    ax=None,
                    show_plot=True,
                    fig_width=5,
                    fig_height=5,
                    fig_dpi=150,
                    vertex_color='#000',
                    edge_color='#000',
                    save_as_file=False,
                    file_directory='',
                    file_name='plot_of_complex',
                    file_extension='png',
                    draw_simplices=True,
                    simplex_alpha=0.2,
                    simplex_color=None,
                    return_fig=True):
    """
    Generates and shows a matplotlib figure of a 3D plot of a simplicial complex.

    Arguments
    ---------
    fig: figure or None, default=None
         Matplotlib figure.
    ax: axis or None, default=None
        Axis of matplotlib figure.
    show_plot: bool, default=True
               If True shows the plot.
    fig_width: float, default=5
               Width of a matplotlib figure.
    fig_height: float, default=5
                Height of a matplotlib figure.
    fig_dpi: float, default=150
             DPI of a matplotlib figure.
    vertex_color: str or list of float, default='#000'
                  Color of vertices.
    edge_color: str or list of float, default='#000'
                Color of edges of a simplicial complex.
    save_as_file: bool, default=False
                  If True then plot is saved as a file instead of being shown.
    file_directory: str, default=''
                    Plot file directory excluding file name and extension.
    file_name: str, default='plot_of_complex'
               Plot file name.
    file_extension: str, default='png'
                    Plot file extension, for list of supported extensions 
                    refer to matplotlib documentation.
    draw_simplices: bool, default=True
                    If True then draws a plot of a simplicial complex by highlighting simplices.
                    If False then draws graph of a simplicial complex by omitting simplices.
    simplex_alpha: float, default=0.2
                   Value corresponding to transparency of simplices.
    simplex_color: None or float or dict of int into float
                   Color of simplices. If None then colors of simplices are randomized 
                   and grouped into respective dimensions. If float then all simplices 
                   share same color. If dict of dimensions p of p-simplices onto colors 
                   then simplices have color assigned by dict.
    """

    if fig is None or ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
    fig.set_figheight(fig_width)
    fig.set_figwidth(fig_height)
    fig.set_dpi(fig_dpi)
    ax.axis('equal')

    vertex_coords = list(complex.vertices.values())

    vertex_coords = np.array(vertex_coords)
    v_x = vertex_coords[:, 0]
    v_y = vertex_coords[:, 1]
    v_z = vertex_coords[:, 2]
    ax.scatter3D(v_x, v_y, v_z, color=vertex_color)

    edges = np.array(complex.graph.edges)
    for vertex_1, vertex_2 in edges:
        v1_x, v1_y, v1_z = complex.vertices[vertex_1]
        v2_x, v2_y, v2_z = complex.vertices[vertex_2]
        ax.plot([v1_x, v2_x], [v1_y, v2_y], [v1_z, v2_z], color=edge_color)
    
    ax.set_xlim((min(v_x)-0.1, max(v_x)+0.1))
    ax.set_ylim((min(v_y)-0.1, max(v_y)+0.1))
    ax.set_zlim((min(v_z)-0.1, max(v_z)+0.1))

    if draw_simplices:
        simplices = [simplex for simplex in complex.simplices if len(simplex) > 2]

        for dim in range(2, complex.dim+1):
            p_simplices = [simplex for simplex in simplices if len(simplex) == dim+1]
            p_simplices_coords = [[complex.vertices[vertex] for vertex in simplex] for simplex in p_simplices]

            if simplex_color is None:
                color = [random.random() for _ in range(3)]
            
            for p_simplex in p_simplices_coords:
                p_simplex = np.array(p_simplex)
                s_x = p_simplex[:, 0]
                s_y = p_simplex[:, 1]
                s_z = p_simplex[:, 2]

                if simplex_color is None:
                    ax.plot_trisurf(s_x, s_y, s_z, color=color, alpha=simplex_alpha)
                elif isinstance(simplex_color, dict):
                    ax.plot_trisurf(s_x, s_y, s_z, color=simplex_color[dim], alpha=simplex_alpha)
                else:
                    ax.plot_trisurf(s_x, s_y, s_z, color=simplex_color, alpha=simplex_alpha)

    if save_as_file:
        plt.savefig(f'{file_directory}{file_name}.{file_extension}')
    if show_plot:
        plt.show()
    if return_fig:
        return fig, ax