import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon
from matplotlib.collections import PatchCollection
import random

def plot_2d_complex(complex,
                    fig_width=5,
                    fig_height=5,
                    fig_dpi=150,
                    with_labels=False,
                    font_size=8,
                    vertex_size=150,
                    vertex_background_color='#fff',
                    vertex_border_color='#000',
                    edge_color='#000',
                    save_as_file=False,
                    file_directory='',
                    file_name='plot_of_complex',
                    file_extension='png',
                    draw_balls=False,
                    ball_alpha=1/5,
                    ball_color=None,
                    draw_simplices=False,
                    simplex_alpha=1/5,
                    simplex_color=None):

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
            node_color=vertex_background_color,
            edge_color=vertex_border_color,
            edgecolors=edge_color)
    
    if draw_balls:
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
            if isinstance(simplex_color, dict):
                patches.set_color(simplex_color[dim])
            else:
                patches.set_color(simplex_color)
            
            patches.set_zorder(-1)
            patches.set_alpha(simplex_alpha)
            
            ax.add_collection(patches)

    plt.tight_layout()

    if save_as_file:
            plt.savefig(f'{file_directory}{file_name}.{file_extension}')
    else:
        plt.show()