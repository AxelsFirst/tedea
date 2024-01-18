import ttkbootstrap as tb
from matplotlib.pyplot import subplots
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from complexes import VietorisRipsComplex
import metrics as m
from plots import plot_2d_complex, plot_3d_complex


class Main_Window(tb.Window):
    """
    Main component of the GUI.

    Parameters
    ----------
    themename: str, default='cerculean'
               Theme provided by ttkbootstrap.

    Attributes
    ----------
    language: str, default='en'
              Currently displayed language.
    vertex_names: list of str
                  Labels of vertices.
    vertex_coords: list of str
                   Coordinates of vertices stored in string format.
    metric: str, default='Euclidean'
            Currently chosen metric stored in string format.
    metric_dict: dict
                 Dictionary for translation of metric string into metric function.
    complex: VietorisRipsComplex
             Instance of Vietoris-Rips complex.
    betti: list of int
           Betti numbers of currently displayed simplicial complex.
    fig: figure
         Matplotlib figure for displaying simplicial complex plot.
    ax: Axis
        Figure axis for placing generated plot.
    draw_graph: tb.BooleanVar
                If True then app generates plot of graph.
    draw_balls: tb.BooleanVar
                If True then app draws balls according to the chosen metric.
    Sidebar: Sidebar
             Sidebar used to place Frames used for customizing simplicial complex.
    Main_Frame: Main_Frame
                Frame used to place other Frames displaying app output.
    """

    def __init__(self, themename='cerculean'):
        """
        Initializes the app, packs most important frames and runs startup complex.

        Arguments
        ---------
        themename: str, default='cerculean'
               Theme provided by ttkbootstrap.
        """

        tb.Window.__init__(self, themename=themename)
        self.title('Tedea')

        self.language = 'en'
        self.vertex_names = []
        self.vertex_coords = []
        self.metric = 'Euclidean'
        self.metric_dict = {
            'Euclidean': m.euclidean_metric,
            'Manhattan': m.manhattan_metric,
            'Maximum': m.maximum_metric,
            'Euklidesowa': m.euclidean_metric,
            'Taksówkarza': m.manhattan_metric,
            'Maksimum': m.maximum_metric
        }
        self.complex = None
        self.betti = None
        self.fig, self.ax = subplots()

        self.startup_complex_plot()

        self.Sidebar = Sidebar(self)
        self.Sidebar.pack(side='left', fill='y')

        self.Main_Frame = Main_Frame(self)
        self.Main_Frame.pack(fill='both', expand=True, padx=10, pady=10)
    
    def startup_complex_plot(self):
        """
        Runs startup simplicial complex for displaying plot. Betti numbers are pregenerated.
        """

        vertex_names = ["A", "B", "C", "D", "E", "F"]
        vertices = [(0, 0), (1, 0), (0, 1), (2, 1), (1, 2), (0.4, 0.4)]
        radius = 0.75

        vr_complex = VietorisRipsComplex(vertices=vertices, 
                                        radius=radius,
                                        vertex_names=vertex_names)

        self.fig, self.ax = plot_2d_complex(vr_complex, 
                                            fig=self.fig, 
                                            ax=self.ax, 
                                            return_fig=True,
                                            show_plot=False)

    def convert_coords_to_float(self):
        """
        Converts vertex_coords from list of str to list of float.
        """

        return [[float(coord) for coord in vertex] for vertex in self.vertex_coords]


class Sidebar(tb.Frame):
    """
    Sidebar used to place Frames used for customizing simplicial complex.

    Parameters
    ----------
    root: Main_Window
          Root upon this Sidebar is packed.
    bootstyle: str, default='light'
               Style of widget.

    Attributes
    ----------
    Main_Window: Main_Window
                 Root upon this Sidebar is packed.
    Title_Frame: Title_Frame
                 Frame for title and language customization.
    Dimension_Frame: Dimension_Frame
                     Frame for choosing dimension of vertices.
    Vertex_Addition_Frame: Vertex_Addition_Frame
                           Frame for adding new vertices.
    Vertex_List_Frame: Vertex_List_Frame
                       Frame for checking and deleting vertices.
    Metric_Frame: Metric_Frame
                  Frame for choosing metric and radius.
    Plot_Config_Frame: Plot_Config_Frame
                       Frame for configuring plots.
    Plot_Generation_Frame: Plot_Generation_Frame
                           Frame for plot generation.
    """

    def __init__(self, root, bootstyle='light'):
        """
        Initializes all frames packed inside Sidebar.

        Parameters
        ----------
        root: Main_Window
            Root upon this Sidebar is packed.
        bootstyle: str, default='light'
                Style of widget.
        """

        tb.Frame.__init__(self, root, bootstyle=bootstyle)
        self.Main_Window = root

        self.Title_Frame = Title_Frame(self)
        self.Title_Frame.pack()

        self.pack_separator()

        self.Dimension_Frame = Dimension_Frame(self)
        self.Dimension_Frame.pack()

        self.pack_separator()

        self.Vertex_Addition_Frame = Vertex_Addition_Frame(self)
        self.Vertex_Addition_Frame.pack()

        self.pack_separator()

        self.Vertex_List_Frame = Vertex_List_Frame(self)
        self.Vertex_List_Frame.pack()

        self.pack_separator()

        self.Metric_Frame = Metric_Frame(self)
        self.Metric_Frame.pack()

        self.pack_separator()

        self.Plot_Config_Frame = Plot_Config_Frame(self)
        self.Plot_Config_Frame.pack()

        self.pack_separator()

        self.Plot_Generation_Frame = Plot_Generation_Frame(self)
        self.Plot_Generation_Frame.pack()

    def pack_separator(self):
        """
        Packs visible separator with primary style.
        """

        separator = tb.Separator(self, bootstyle='primary')
        separator.pack(fill='x', padx=15, pady=25)


class Sidebar_Frame(tb.Frame):
    """
    Template for other frames placed in Sidebar.

    Parameters
    ----------
    root: Sidebar
          Root upon this frame is packed.
    bootstyle: str, default='light'
               Style of widget.
    
    Attributes
    ----------
    Main_Window: Main_Window
                 Main window of the app.
    Sidebar: Sidebar
             Sidebar this frame is packed upon.
    """

    def __init__(self, root, bootstyle='light'):
        """
        Initializes the frame and sets the style.
        """

        tb.Frame.__init__(self, root, bootstyle=bootstyle)
        self.Main_Window = root.Main_Window
        self.Sidebar = root
    
    def pack_hidden_separator(self, bootstyle='light'):
        """
        Packs hidden separator for spacing.
        """

        separator = tb.Separator(self, bootstyle=bootstyle)
        separator.pack(pady=5)
    
    def grid_hidden_separator(self, row, column, columnspan, bootstyle='light'):
        """
        Grids hidden separator for spacing.
        """

        separator = tb.Separator(self, bootstyle=bootstyle)
        separator.grid(row=row, column=column, columnspan=columnspan, pady=5)


class Title_Frame(Sidebar_Frame):
    """
    Frame for title and language customization.
    
    Parameters
    ----------
    root: Sidebar
          Root upon this frame is packed.
    bootstyle: str, default='light'
               Style of widget.
    
    Attributes
    ----------
    Main_Window: Main_Window
                 Main window of the app.
    Sidebar: Sidebar
             Sidebar this frame is packed upon.
    side_label: tb.Label
                Title label.
    self.button_language: tb.Button
                          Button for changing the displayed language.
    """

    def __init__(self, root):
        """
        Initializes all widgets packed inside.

        Arguments
        ---------
        root: Main_Window
            Root upon this Sidebar is packed.
        bootstyle: str, default='light'
                Style of widget.
        """

        Sidebar_Frame.__init__(self, root)

        self.side_label = tb.Label(self, 
                                   text='Simplicial Complex Settings', 
                                   bootstyle='inverse-light')
        self.side_label.config(font=('', 12))
        self.side_label.pack(pady=15, padx=20)

        self.button_language = tb.Button(self,
                                         text='[English] Change language',
                                         bootstyle='info',
                                         command=self.change_language)
        self.button_language.pack()

    def change_language(self):
        """
        Changes the displayed language by swapping all visible texts.
        """

        Dimension_Frame = self.Sidebar.Dimension_Frame
        Vertex_Addition_Frame = self.Sidebar.Vertex_Addition_Frame
        Vertex_List_Frame = self.Sidebar.Vertex_List_Frame
        Metric_Frame = self.Sidebar.Metric_Frame
        Plot_Config_Frame = self.Sidebar.Plot_Config_Frame
        Plot_Generation_Frame = self.Sidebar.Plot_Generation_Frame
        Plot_Frame = self.Main_Window.Main_Frame.Plot_Frame
        Betti_Frame = self.Main_Window.Main_Frame.Betti_Frame

        if self.Main_Window.language == 'en':
            self.Main_Window.language = 'pl'
            
            self.side_label.config(text='Ustawienia Kompleksu Symplicjalnego')
            self.button_language.config(text='[Polski] Zmień język')

            Dimension_Frame.label_dimension.config(text='Podaj wymiar przestrzeni:')

            Vertex_Addition_Frame.label_name.config(text='Podaj etykietę wierzchołka:')
            Vertex_Addition_Frame.label_coords.config(text='Podaj współrzędne wierzchołka:')
            Vertex_Addition_Frame.button_confirmation.config(text='Potwierdź wierzchołek')

            Vertex_List_Frame.menubutton_vertex.config(text='Dodane wierzchołki')
            Vertex_List_Frame.button_deletion.config(text='Usuń wierzchołek')

            Metric_Frame.menu_metric = tb.Menu(Metric_Frame.menubutton_metric)

            self.Main_Window.metric = 'Euklidesowa'
            Metric_Frame.menubutton_metric.config(text='Wybierz metrykę')
            Metric_Frame.available_metrics = ['Euklidesowa', 'Taksówkarza', 'Maksimum']
            for metric in Metric_Frame.available_metrics:
                Metric_Frame.menu_metric.add_radiobutton(
                    label=metric, 
                    command= lambda x=metric: Metric_Frame.set_metric(metric=x))
                
            Metric_Frame.menubutton_metric['menu'] = Metric_Frame.menu_metric

            Metric_Frame.label_radius.config(text='Podaj promień:')

            Plot_Config_Frame.toggle_graph.config(text='Rysuj graf')
            Plot_Config_Frame.toggle_balls.config(text='Rysuj kule')

            Plot_Generation_Frame.button_generation.config(text='Wygeneruj wykres')
            if Dimension_Frame.entry_dimension.get().isdecimal():
                dim = int(Dimension_Frame.entry_dimension.get())
                if dim != 2 and dim != 3:
                    self.Sidebar.Plot_Generation_Frame.button_generation.config(text='Oblicz liczby Bettiego')
            Plot_Generation_Frame.button_save.config(text='Zapisz wykres')

            Plot_Frame.config(text='Wykres')

            Betti_Frame.config(text='Liczby Bettiego')
        else:
            self.Main_Window.language = 'en'

            self.side_label.config(text='Simplicial Complex Settings')
            self.button_language.config(text='[English] Change language')

            Dimension_Frame.label_dimension.config(text='Enter dimension of space:')

            Vertex_Addition_Frame.label_name.config(text='Enter vertex label:')
            Vertex_Addition_Frame.label_coords.config(text='Enter vertex coordinates:')
            Vertex_Addition_Frame.button_confirmation.config(text='Confirm vertex')

            Vertex_List_Frame.menubutton_vertex.config(text='Added vertices')
            Vertex_List_Frame.button_deletion.config(text='Delete vertices')

            Metric_Frame.menu_metric = tb.Menu(Metric_Frame.menubutton_metric)

            self.Main_Window.metric = 'Euclidean'
            Metric_Frame.menubutton_metric.config(text='Choose metric')
            Metric_Frame.available_metrics = ['Euclidean', 'Manhattan', 'Maximum']
            for metric in Metric_Frame.available_metrics:
                Metric_Frame.menu_metric.add_radiobutton(
                    label=metric, 
                    command= lambda x=metric: Metric_Frame.set_metric(metric=x))
                
            Metric_Frame.menubutton_metric['menu'] = Metric_Frame.menu_metric

            Metric_Frame.label_radius.config(text='Enter radius:')

            Plot_Config_Frame.toggle_graph.config(text='Draw graph')
            Plot_Config_Frame.toggle_balls.config(text='Draw balls')

            Plot_Generation_Frame.button_generation.config(text='Generate plot')
            if Dimension_Frame.entry_dimension.get().isdecimal():
                dim = int(Dimension_Frame.entry_dimension.get())
                if dim != 2 and dim != 3:
                    self.Sidebar.Plot_Generation_Frame.button_generation.config(text='Calculate Betti numbers')
            Plot_Generation_Frame.button_save.config(text='Save plot')

            Plot_Frame.config(text='Plot')

            Betti_Frame.config(text='Betti Numbers')


class Dimension_Frame(Sidebar_Frame):
    """
    Frame for choosing dimension of vertices.

    Parameters
    ----------
    root: Sidebar
          Root upon this frame is packed.
    bootstyle: str, default='light'
               Style of widget.
    
    Attributes
    ----------
    Main_Window: Main_Window
                 Main window of the app.
    Sidebar: Sidebar
             Sidebar this frame is packed upon.
    label_dimension: tb.Label
                     Label for entry_dimension.
    entry_dimension: tb.Entry
                     Entry for getting dimension of vertices.
    """

    def __init__(self, root):
        """
        Initializes all widgets packed inside.

        Arguments
        ---------
        root: Main_Window
            Root upon this Sidebar is packed.
        bootstyle: str, default='light'
                Style of widget.
        """

        Sidebar_Frame.__init__(self, root)

        self.label_dimension = tb.Label(self, text='Enter dimension of space:', bootstyle='inverse-light')
        self.label_dimension.pack()

        validation_dimension = self.Main_Window.register(self.validate_dimension)

        self.entry_dimension = tb.Entry(self, validate='focusout', validatecommand=(validation_dimension, '%P'))
        self.entry_dimension.pack()
    
    def validate_dimension(self, dim):
        """
        Validates entry_dimension output by checking characters. Autodisables uncompatible options.

        Arguments
        ---------
        dim: str
             Output from entry_dimension.

        Returns
        -------
        validated: bool
                   True if dim is an integer.
        """

        if dim.isdecimal():
            if int(dim) == 2:
                self.Sidebar.Plot_Config_Frame.toggle_graph.config(state='normal')
                self.Sidebar.Plot_Config_Frame.toggle_balls.config(state='normal')

                self.Sidebar.Plot_Generation_Frame.button_save.config(state='normal')
                if self.Main_Window.language == 'en':
                    self.Sidebar.Plot_Generation_Frame.button_generation.config(text='Generate plot')
                else:
                    self.Sidebar.Plot_Generation_Frame.button_generation.config(text='Wygeneruj wykres')

                return True
            elif int(dim) == 3:
                self.Sidebar.Plot_Config_Frame.toggle_graph.config(state='normal')
                self.Sidebar.Plot_Config_Frame.toggle_balls.config(state='disabled')

                self.Sidebar.Plot_Generation_Frame.button_save.config(state='normal')
                if self.Main_Window.language == 'en':
                    self.Sidebar.Plot_Generation_Frame.button_generation.config(text='Generate plot')
                else:
                    self.Sidebar.Plot_Generation_Frame.button_generation.config(text='Wygeneruj wykres')

                return True
            else:
                self.Sidebar.Plot_Config_Frame.toggle_graph.config(state='disabled')
                self.Sidebar.Plot_Config_Frame.toggle_balls.config(state='disabled')

                self.Sidebar.Plot_Generation_Frame.button_save.config(state='disabled')
                if self.Main_Window.language == 'en':
                    self.Sidebar.Plot_Generation_Frame.button_generation.config(text='Calculate Betti numbers')
                else:
                    self.Sidebar.Plot_Generation_Frame.button_generation.config(text='Oblicz liczby Bettiego')
                
                if int(dim) == 0:
                    return False
                else:
                    return True
        else:
            return False


class Vertex_Addition_Frame(Sidebar_Frame):
    """
    Frame for adding new vertices.

    Parameters
    ----------
    root: Sidebar
          Root upon this frame is packed.
    bootstyle: str, default='light'
               Style of widget.
    
    Attributes
    ----------
    Main_Window: Main_Window
                 Main window of the app.
    Sidebar: Sidebar
             Sidebar this frame is packed upon.
    label_name: tb.Label
                Label for entry_name.
    entry_name: tb.Entry
                Entry for getting vertex name.
    label_coords: tb.Label
                  Label for entry_coords.
    entry_coords: tb.Entry
                  Entry for getting coords spaced out by one space.
    button_confirmation: tb.Button
                         Confirmation of addition of new vertex. 
                         Clears out entries upon being pressed.
    """

    def __init__(self, root):
        """
        Initializes all widgets packed inside.

        Arguments
        ---------
        root: Main_Window
            Root upon this Sidebar is packed.
        bootstyle: str, default='light'
                Style of widget.
        """

        Sidebar_Frame.__init__(self, root)

        self.label_name = tb.Label(self, 
                                   text='Enter vertex label:', 
                                   bootstyle='inverse-light')
        self.label_name.pack()

        validation_name = self.Main_Window.register(self.validate_name)

        self.entry_name = tb.Entry(self,
                                   validate='focusout',
                                   validatecommand=(validation_name, '%P'))
        self.entry_name.pack()

        self.pack_hidden_separator()

        self.label_coords = tb.Label(self, 
                                     text='Enter vertex coordinates:', 
                                     bootstyle='inverse-light')
        self.label_coords.pack()

        validation_coords = self.Main_Window.register(self.validate_coords)

        self.entry_coords = tb.Entry(self, 
                                     validate='focusout', 
                                     validatecommand=(validation_coords, '%P'))
        self.entry_coords.pack()

        self.pack_hidden_separator()

        self.button_confirmation = tb.Button(self, 
                                             text='Confirm vertex', 
                                             bootstyle='primary', 
                                             command=self.vertex_confirmation)
        self.button_confirmation.pack(pady=10)

    def validate_name(self, name):
        """
        Validates name by checking its uniqueness.

        Arguments
        ---------
        name: str
              Name of vertex.

        Returns
        -------
        validated: bool
                   True if name is unique.
        """

        if name == '' or name in self.Main_Window.vertex_names:
            return False
        else:
            return True

    def validate_coords(self, coords_text):
        """
        Validates coordinates by checking their type, their amount and uniqueness.

        Arguments
        ---------
        coords_text: str
                     Coordinates stored in one string.

        Returns
        -------
        validated: bool
                   True if correct type, amount and if is unique.
        """

        coords = coords_text.replace(',', '').split(' ')
        dim = self.Sidebar.Dimension_Frame.entry_dimension.get()
        
        if not dim.isdecimal():
            return False
        elif len(coords) != int(dim):
            return False
        
        for coord in coords:
            if not coord.replace('.', '').isdecimal():
                return False
        
        if coords in self.Main_Window.vertex_coords:
            return False
        
        return True
    
    def get_coords(self):
        """
        Get coordinates from entry as a list of str.

        Returns
        -------
        coords: list of str
                Coordinates from entry.
        """

        coords_text = self.entry_coords.get()
        coords = coords_text.replace(',', '.').split(' ')
        return coords
    
    def get_str_coords(self):
        """
        Get coordinates from entry as a single string.

        Returns
        -------
        coords: str
                Coordinates from entry.
        """

        coords_text = self.entry_coords.get()
        coords = coords_text.replace(',', '.')
        return coords
    
    def clear_entries(self):
        """
        Clears entry_name and entry_coords.
        """

        self.entry_name.delete(0, len(self.entry_name.get()))
        self.entry_coords.delete(0, len(self.entry_coords.get()))

    def vertex_confirmation(self):
        """
        Last check and addition of new vertex to the list of vertices.
        """

        vertex_name = self.entry_name.get()
        unique_name = self.validate_name(vertex_name)

        dim_text = self.Sidebar.Dimension_Frame.entry_dimension.get()
        dim_chosen = self.Sidebar.Dimension_Frame.validate_dimension(dim_text)

        coords_txt = self.get_str_coords()
        coords_validated = self.validate_coords(coords_txt)
        
        if unique_name and dim_chosen and coords_validated:
            self.Main_Window.vertex_names.append(vertex_name)
            self.Main_Window.vertex_coords.append(self.get_coords())

            Vertex_List_Frame = self.Sidebar.Vertex_List_Frame

            coords_text = self.get_str_coords()
            text = f'{vertex_name}: {coords_text}'

            Vertex_List_Frame.menu_vertex.add_radiobutton(
                label=text,
                command= lambda x=text: Vertex_List_Frame.waitlist(x)
            )

            self.clear_entries()


class Vertex_List_Frame(Sidebar_Frame):
    """
    Frame for checking and deleting vertices.

    Parameters
    ----------
    root: Sidebar
          Root upon this frame is packed.
    bootstyle: str, default='light'
               Style of widget.
    
    Attributes
    ----------
    Main_Window: Main_Window
                 Main window of the app.
    Sidebar: Sidebar
             Sidebar this frame is packed upon.
    vertex_to_delete: list of str
                      List of vertices to delete.
    menubutton_vertex: tb.Menubutton
                       Button for showing menu_vertex.
    menu_vertex: tb.Menu
                 List of previously added vertices. 
                 Check vertices to flag them for deletion.
    button_deletion: tb.Button
                     Button for deletion of all flagged vertices.
    """

    def __init__(self, root):
        """
        Initializes all widgets packed inside.

        Arguments
        ---------
        root: Main_Window
            Root upon this Sidebar is packed.
        bootstyle: str, default='light'
                Style of widget.
        """

        Sidebar_Frame.__init__(self, root)
        self.vertex_to_delete = ''

        self.menubutton_vertex = tb.Menubutton(self, 
                                               text='Added vertices', 
                                               bootstyle='secondary')
        self.menubutton_vertex.pack()

        self.menu_vertex = tb.Menu(self.menubutton_vertex)

        self.menubutton_vertex['menu'] = self.menu_vertex

        self.pack_hidden_separator()

        self.button_deletion = tb.Button(self, 
                                         text='Delete vertices', 
                                         bootstyle='primary',
                                         command=self.vertex_deletion)
        self.button_deletion.pack()

    def waitlist(self, vertex):
        """
        Flags or unflags vertices for deletion.        
        """

        self.vertex_to_delete = vertex

    def vertex_deletion(self):
        """
        Deletes flagged vertices and create new list of remaining vertices.
        """

        vertex_txt = self.vertex_to_delete

        if vertex_txt != '':
            vertex_name = vertex_txt.split(':')[0]
            vertex_index = self.Main_Window.vertex_names.index(vertex_name)

            self.Main_Window.vertex_names.pop(vertex_index)
            self.Main_Window.vertex_coords.pop(vertex_index)

            self.vertex_to_delete = ''

            self.menu_vertex = tb.Menu(self.menubutton_vertex)

            for index in range(len(self.Main_Window.vertex_names)):
                remaining_vertex_name = self.Main_Window.vertex_names[index]
                remaining_vertex_coords = self.Main_Window.vertex_coords[index]

                remaining_vertex_coords_txt = ''
                for coord_index in range(len(remaining_vertex_coords)-1):
                    remaining_vertex_coords_txt += remaining_vertex_coords[coord_index]+' '
                remaining_vertex_coords_txt += remaining_vertex_coords[-1]

                text = f'{remaining_vertex_name}: {remaining_vertex_coords_txt}'

                self.menu_vertex.add_radiobutton(
                    label=text,
                    command= lambda x=text: self.waitlist(x)
                )

            self.menubutton_vertex['menu'] = self.menu_vertex


class Metric_Frame(Sidebar_Frame):
    """
    Frame for choosing metric and radius.

    Parameters
    ----------
    root: Sidebar
          Root upon this frame is packed.
    bootstyle: str, default='light'
               Style of widget.
    
    Attributes
    ----------
    Main_Window: Main_Window
                 Main window of the app.
    Sidebar: Sidebar
             Sidebar this frame is packed upon.
    menubutton_metric: tb.Menubutton
                       Button for showing menu_metric.
    menu_metric: tb.Menu
                 Menu displaying available metrics.
    available_metrics: list of str
                       List of available metrics.
    label_radius: tb.Label
                  Label for entry_radius.
    entry_radius: tb.Entry
                  Entry for getting radius.
    """

    def __init__(self, root):
        Sidebar_Frame.__init__(self, root)

        self.menubutton_metric = tb.Menubutton(self, 
                                               text='Choose metric', 
                                               bootstyle='secondary')
        self.menubutton_metric.pack()

        self.menu_metric = tb.Menu(self.menubutton_metric)
        self.available_metrics = ['Euclidean', 'Manhattan', 'Maximum']
        for metric in self.available_metrics:
            self.menu_metric.add_radiobutton(label=metric, 
                                             command= lambda x=metric: self.set_metric(metric=x))

        self.menubutton_metric['menu'] = self.menu_metric

        self.pack_hidden_separator()

        self.label_radius = tb.Label(self, 
                                     text='Enter radius:', 
                                     bootstyle='inverse-light')
        self.label_radius.pack()

        validation_radius = self.Main_Window.register(self.validate_radius)

        self.entry_radius = tb.Entry(self, 
                                     validate='focusout', 
                                     validatecommand=(validation_radius, '%P'))
        self.entry_radius.pack()

    def set_metric(self, metric):
        """
        Initializes all widgets packed inside.

        Arguments
        ---------
        root: Main_Window
            Root upon this Sidebar is packed.
        bootstyle: str, default='light'
                Style of widget.
        """

        self.menubutton_metric.config(text=metric)
        self.Main_Window.metric = metric

    def validate_radius(self, radius):
        """
        Validates radius by checking their value.

        Arguments
        ---------
        radius: str
                Radius stored in string.

        Returns
        -------
        validated: bool
                   True if correct type.
        """
        radius = radius.replace(',', '').replace('.', '')
        if radius.isdecimal():
            return True
        else:
            return False
        

class Plot_Config_Frame(Sidebar_Frame):
    """
    Frame for configuring plots.

    Parameters
    ----------
    root: Sidebar
          Root upon this frame is packed.
    bootstyle: str, default='light'
               Style of widget.
    
    Attributes
    ----------
    Main_Window: Main_Window
                 Main window of the app.
    Sidebar: Sidebar
             Sidebar this frame is packed upon.
    toggle_graph: tb.Checkbutton
                  Toggle drawing graph instead of a complex.
    toogle_balls: tb.Checkbutton
                  Toggle drawing balls on plot.
    """

    def __init__(self, root):
        """
        Initializes all widgets packed inside.

        Arguments
        ---------
        root: Main_Window
            Root upon this Sidebar is packed.
        bootstyle: str, default='light'
                Style of widget.
        """

        Sidebar_Frame.__init__(self, root)

        self.Main_Window.draw_graph = tb.BooleanVar()
        self.toggle_graph = tb.Checkbutton(self, 
                                           bootstyle="secondary-outline-toolbutton", 
                                           text='Draw graph',
                                           variable=self.Main_Window.draw_graph)
        self.toggle_graph.grid(row=0, column=0)

        self.Main_Window.draw_balls = tb.BooleanVar()
        self.toggle_balls = tb.Checkbutton(self, 
                                           bootstyle="secondary-outline-toolbutton", 
                                           text='Draw balls',
                                           variable=self.Main_Window.draw_balls)
        self.toggle_balls.grid(row=0, column=1)


class Plot_Generation_Frame(Sidebar_Frame):
    """
    Frame for plot generation.

    Parameters
    ----------
    root: Sidebar
          Root upon this frame is packed.
    bootstyle: str, default='light'
               Style of widget.
    
    Attributes
    ----------
    Main_Window: Main_Window
                 Main window of the app.
    Sidebar: Sidebar
             Sidebar this frame is packed upon.
    plot_generation: register(function)
                     Function for plot generation.
    button_generation: tb.Button
                       Button for starting the plot generation process.
    plot_saving: register(function)
                 Function for saving generated plot.
    button_save: tb.Button
                 Button for starting the plot saving process.
    """

    def __init__(self, root):
        """
        Initializes all widgets packed inside.

        Arguments
        ---------
        root: Main_Window
            Root upon this Sidebar is packed.
        bootstyle: str, default='light'
                Style of widget.
        """

        Sidebar_Frame.__init__(self, root)

        self.plot_generation = self.Main_Window.register(self.generate_plot)
        self.button_generation = tb.Button(self, 
                                           bootstyle='success', 
                                           text='Generate plot',
                                           command=self.plot_generation)
        self.button_generation.grid(row=0, column=0)

        self.plot_saving = self.Main_Window.register(self.save_plot)
        self.button_save = tb.Button(self, 
                                     bootstyle='primary', 
                                     text='Save plot',
                                     command=self.plot_saving)
        self.button_save.grid(row=0, column=1)

        self.grid_hidden_separator(row=1, column=1, columnspan=2)
    
    def check_input(self):
        """
        Checks if all input from entries is correct.

        Returns
        -------
        validated: bool
                   If True then data is correct.
        """

        dim = self.Sidebar.Dimension_Frame.entry_dimension.get()
        dim_validated = self.Sidebar.Dimension_Frame.validate_dimension(dim)

        added_vertices = self.Main_Window.vertex_coords
        if_added_vertices = len(added_vertices) > 0

        radius = self.Sidebar.Metric_Frame.entry_radius.get()
        radius_validated = self.Sidebar.Metric_Frame.validate_radius(radius)

        if dim_validated and if_added_vertices and radius_validated:
            for vertex in added_vertices:
                if len(vertex) != int(dim):
                    return False
            return True
        else:
            False


    def generate_plot(self):
        """
        Generates the plot and starts the process of updating plot canvas and Betti label.
        """

        radius = self.Sidebar.Metric_Frame.entry_radius.get()

        if self.check_input():
            vertex_coords = self.Main_Window.convert_coords_to_float()

            metric_func = self.Main_Window.metric_dict[self.Main_Window.metric]

            radius = float(radius)

            self.Main_Window.complex = VietorisRipsComplex(
                vertices=vertex_coords,
                vertex_names=self.Main_Window.vertex_names,
                radius=radius,
                metric=metric_func
            )
            
            self.Main_Window.Main_Frame.Plot_Frame.update_canvas()

            self.Main_Window.betti = self.Main_Window.complex.get_betti()

            self.Main_Window.Main_Frame.Betti_Frame.update_betti()
    
    def save_plot(self):
        """
        Saves plot to app directory.
        """

        if self.check_input():
            dim = self.Sidebar.Dimension_Frame.entry_dimension.get()

            if int(dim) == 2:
                draw_balls = self.Main_Window.draw_balls.get()
                draw_simplices = not self.Main_Window.draw_graph.get()

                plot_2d_complex(
                    self.Main_Window.complex,
                    draw_balls=draw_balls,
                    draw_simplices=draw_simplices,
                    save_as_file=True,
                    return_fig=False,
                    show_plot=False
                )

            elif int(dim) == 3:
                draw_simplices = not self.Main_Window.draw_graph.get()

                self.Main_Window.fig, self.Main_Window.ax = plot_3d_complex(
                    self.Main_Window.complex,
                    draw_simplices=draw_simplices,
                    save_as_file=True,
                    return_fig=True,
                    show_plot=False
                )


class Main_Frame(tb.Frame):
    """
    Frame used to place other Frames displaying app output.

    Parameters
    ----------
    root: Main_Window
          Root upon this Sidebar is packed.
    bootstyle: str, default='default'
               Style of widget.

    Attributes
    ----------
    Main_Window: Main_Window
                 Root upon this Main_Frame is packed.
    Plot_Frame: Plot_Frame
                Frame for packing plot canvas.
    Betti_Frame: Betti_Frame
                 Frame for displaying Betti numbers.
    """

    def __init__(self, root, bootstyle='default'):
        """
        Initializes all frames packed inside Main_Frame.

        Parameters
        ----------
        root: Main_Window
            Root upon this Sidebar is packed.
        bootstyle: str, default='default'
                Style of widget.
        """

        tb.Frame.__init__(self, root, bootstyle=bootstyle)
        self.Main_Window = root

        self.Plot_Frame = Plot_Frame(self)
        self.Plot_Frame.pack(fill='both', expand=True, pady=5)

        self.Betti_Frame = Betti_Frame(self)
        self.Betti_Frame.pack(fill='both', expand=True, pady=5, ipady=4)


class Plot_Frame(tb.Labelframe):
    """
    Frame for packing plot canvas.

    Parameters
    ----------
    root: Main_Frame
          Root upon this frame is packed.
    bootstyle: str, default='default'
               Style of widget.

    Attributes
    ----------
    Main_Window: Main_Window
                 Root upon this Main_Frame is packed.
    Sidebar: Sidebar
             Sidebar for getting data.
    canvas: FigureCanvasTkAgg
            Matplotlib plot embedded into app.
    """

    def __init__(self, root, bootstyle='default'):
        """
        Initializes all widgets packed inside.

        Arguments
        ---------
        root: Main_Frame
              Root upon this frame is packed.
        bootstyle: str, default='default'
                   Style of widget.
        """
        tb.Labelframe.__init__(self, root, text='Plot', bootstyle='default')
        self.Main_Window = root.Main_Window
        self.Sidebar = self.Main_Window.Sidebar
        
        self.canvas = FigureCanvasTkAgg(self.Main_Window.fig, self)
        self.canvas.draw()
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side='left', fill='both', expand=True)
    
    def update_canvas(self):
        """
        Updates the canvas by deleting it and packing a new canvas.
        """

        self.Main_Window.ax.clear()

        dim = self.Sidebar.Dimension_Frame.entry_dimension.get()

        if int(dim) == 2:
            draw_balls = self.Main_Window.draw_balls.get()
            draw_simplices = not self.Main_Window.draw_graph.get()

            metric = self.Main_Window.metric_dict[self.Main_Window.metric]

            self.Main_Window.fig, self.Main_Window.ax = plot_2d_complex(
                self.Main_Window.complex,
                draw_balls=draw_balls,
                draw_simplices=draw_simplices,
                metric=metric,
                return_fig=True,
                show_plot=False
            )

            self.canvas_widget.destroy()

            self.canvas = FigureCanvasTkAgg(self.Main_Window.fig, self)
            self.canvas.draw()
            self.canvas_widget = self.canvas.get_tk_widget()
            self.canvas_widget.pack(side='left', fill='both', expand=True)

        elif int(dim) == 3:
            draw_simplices = not self.Main_Window.draw_graph.get()

            self.Main_Window.fig, self.Main_Window.ax = plot_3d_complex(
                self.Main_Window.complex,
                draw_simplices=draw_simplices,
                return_fig=True,
                show_plot=False
            )

            self.canvas_widget.destroy()

            self.canvas = FigureCanvasTkAgg(self.Main_Window.fig, self)
            self.canvas.draw()
            self.canvas_widget = self.canvas.get_tk_widget()
            self.canvas_widget.pack(side='left', fill='both', expand=True)
        
        else:
            self.Main_Window.fig, self.Main_Window.ax = subplots()

            self.canvas_widget.destroy()

            self.canvas = FigureCanvasTkAgg(self.Main_Window.fig, self)
            self.canvas.draw()
            self.canvas_widget = self.canvas.get_tk_widget()
            self.canvas_widget.pack(side='left', fill='both', expand=True)


class Betti_Frame(tb.LabelFrame):
    """
    Frame for displaying Betti numbers.

    Parameters
    ----------
    root: Main_Frame
          Root upon this frame is packed.
    bootstyle: str, default='default'
               Style of widget.

    Attributes
    ----------
    Main_Window: Main_Window
                 Root upon this Main_Frame is packed.
    betti_label: tb.Label
                 Displays Betti numbers of plotted simplicial complex.
    """

    def __init__(self, root, text='Betti Numbers', bootstyle='default'):
        """
        Initializes all widgets packed inside.

        Arguments
        ---------
        root: Main_Frame
              Root upon this frame is packed.
        bootstyle: str, default='default'
                   Style of widget.
        """

        tb.LabelFrame.__init__(self, root, text=text, bootstyle=bootstyle)
        self.Main_Window = root.Main_Window

        self.betti_label = tb.Label(self, 
                                    text='\u03B2_0 = 1, \u03B2_1 = 1, \u03B2_2 = 0, \u03B2_3 = 0')
        self.betti_label.config(font=('', 12))
        self.betti_label.pack()

    def update_betti(self):
        """
        Updates betti_label.
        """

        betti = self.Main_Window.betti
        
        for i in range(len(betti)-1):
            betti[i] = f'\u03B2_{i} = {betti[i]}, '
        betti[-1] = f'\u03B2_{len(betti)-1} = {betti[-1]}'

        betti_txt = ''.join(betti)

        self.betti_label.config(text=betti_txt)


if __name__ == '__main__':
    app = Main_Window()
    app.mainloop()