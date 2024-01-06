# from complexes import *
import matplotlib.pyplot as plt

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
                    file_extension='png'):

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
                
    plt.tight_layout()

    if save_as_file:
            plt.savefig(f'{file_directory}{file_name}.{file_extension}')
    else:
        plt.show()