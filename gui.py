import ttkbootstrap as tb
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from complexes import VietorisRipsComplex
from plots import plot_2d_complex


class Main_Window(tb.Window):
    def __init__(self, themename='cerculean'):
        tb.Window.__init__(self, themename=themename)
        self.title('Tedea')

        self.dim = None
        self.vertex_names = []
        self.vertex_coords = []
        self.metric = 'Euclidean'
        self.complex = None
        self.fig = None
        self.betti = None

        self.Sidebar = Sidebar(self)
        self.Sidebar.pack(side='left', fill='y')

        self.Main_Frame = Main_Frame(self, fig)
        self.Main_Frame.pack(fill='both', expand=True, padx=10, pady=10)


class Sidebar(tb.Frame):
    def __init__(self, root, bootstyle='light'):
        tb.Frame.__init__(self, root, bootstyle=bootstyle)
        self.Main_Window = root

        self.side_label = tb.Label(self, 
                                   text='Simplicial Complex Settings', 
                                   bootstyle='inverse-light')
        self.side_label.pack(pady=20, padx=20)

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
        separator = tb.Separator(self, bootstyle='primary')
        separator.pack(fill='x', padx=15, pady=25)


class Sidebar_Frame(tb.Frame):
    def __init__(self, root, bootstyle='light'):
        tb.Frame.__init__(self, root, bootstyle=bootstyle)
        self.Main_Window = root.Main_Window
        self.Sidebar = root
    
    def pack_hidden_separator(self, bootstyle='light'):
        separator = tb.Separator(self, bootstyle=bootstyle)
        separator.pack(pady=5)
    
    def grid_hidden_separator(self, row, column, columnspan, bootstyle='light'):
        separator = tb.Separator(self, bootstyle=bootstyle)
        separator.grid(row=row, column=column, columnspan=columnspan, pady=5)


class Dimension_Frame(Sidebar_Frame):
    def __init__(self, root):
        Sidebar_Frame.__init__(self, root)

        label_dimension = tb.Label(self, text='Enter dimension of vertices:', bootstyle='inverse-light')
        label_dimension.pack()

        validation_dimension = self.Main_Window.register(self.validate_dimension)

        self.entry_dimension = tb.Entry(self, validate='focusout', validatecommand=(validation_dimension, '%P'))
        self.entry_dimension.pack()
    
    def validate_dimension(self, dim):
        if dim.isdecimal():
            return True
        else:
            return False


class Vertex_Addition_Frame(Sidebar_Frame):
    def __init__(self, root):
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
        if name in self.Main_Window.vertex_names:
            return False
        else:
            return True

    def validate_coords(self, coords_text):
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
        coords_text = self.entry_coords.get()
        coords = coords_text.replace(',', '.').split(' ')
        return coords
    
    def clear_entries(self):
        self.entry_name.delete(0, len(self.entry_name.get()))
        self.entry_coords.delete(0, len(self.entry_coords.get()))

    def vertex_confirmation(self):
        vertex_name = self.entry_name.get()
        unique_name = self.validate_name(vertex_name)
        dim_text = self.Sidebar.Dimension_Frame.entry_dimension.get()
        dim_chosen = self.Sidebar.Dimension_Frame.validate_dimension(dim_text)
        
        if unique_name and dim_chosen:
            self.Main_Window.vertex_names.append(vertex_name)
            self.Main_Window.vertex_coords.append(self.get_coords())

            Vertex_List_Frame = self.Sidebar.Vertex_List_Frame

            Vertex_List_Frame.menu_vertex.add_checkbutton(
                label=vertex_name,
                command= lambda x=vertex_name: Vertex_List_Frame.waitlist(x)
            )

            self.clear_entries()


class Vertex_List_Frame(Sidebar_Frame):
    def __init__(self, root):
        Sidebar_Frame.__init__(self, root)
        self.vertices_to_delete = []

        self.menubutton_vertex = tb.Menubutton(self, 
                                               text='Added vertices', 
                                               bootstyle='primary')
        self.menubutton_vertex.pack()

        self.menu_vertex = tb.Menu(self.menubutton_vertex)

        self.menubutton_vertex['menu'] = self.menu_vertex # create a function to refresh it every new vertex

        self.pack_hidden_separator()

        self.button_deletion = tb.Button(self, 
                                         text='Delete vertices', 
                                         bootstyle='primary',
                                         command=self.vertex_deletion)
        self.button_deletion.pack()

    def waitlist(self, vertex):
        if vertex in self.vertices_to_delete:
            self.vertices_to_delete.remove(vertex)
        else:
            self.vertices_to_delete.append(vertex)

    def vertex_deletion(self):
        vertex_indices = []
        for vertex in self.vertices_to_delete:
            index = self.Main_Window.vertex_names.index(vertex)
            vertex_indices.append(index)

        for index in sorted(vertex_indices, reverse=True):
            self.Main_Window.vertex_names.pop(index)
            self.Main_Window.vertex_coords.pop(index)
        
        self.vertices_to_delete = []

        self.menu_vertex = tb.Menu(self.menubutton_vertex)
        for vertex in self.Main_Window.vertex_names:
            self.menu_vertex.add_checkbutton(
                label=vertex,
                command= lambda x=vertex: Vertex_List_Frame.waitlist(x)
            )
        
        self.menubutton_vertex['menu'] = self.menu_vertex


class Metric_Frame(Sidebar_Frame):
    def __init__(self, root):
        Sidebar_Frame.__init__(self, root)

        self.menubutton_metric = tb.Menubutton(self, 
                                               text='Choose metric', 
                                               bootstyle='primary')
        self.menubutton_metric.pack()

        self.menu_metric = tb.Menu(self.menubutton_metric)
        for metric in ['Euclidean', 'Manhattan', 'Maximum']:
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
        self.menubutton_metric.config(text=metric)
        self.Main_Window.metric = metric

    def validate_radius(self, radius):
        radius = radius.replace(',', '').replace('.', '')
        if radius.isdecimal():
            return True
        else:
            return False
        

class Plot_Config_Frame(Sidebar_Frame):
    def __init__(self, root):
        Sidebar_Frame.__init__(self, root)

        self.Main_Window.draw_graph = tb.BooleanVar()
        self.toggle_graph = tb.Checkbutton(self, 
                                           bootstyle="outline-toolbutton", 
                                           text='Draw graph',
                                           variable=self.Main_Window.draw_graph)
        self.toggle_graph.grid(row=0, column=0)

        self.Main_Window.draw_balls = tb.BooleanVar()
        self.toggle_balls = tb.Checkbutton(self, 
                                           bootstyle="outline-toolbutton", 
                                           text='Draw balls',
                                           variable=self.Main_Window.draw_balls)
        self.toggle_balls.grid(row=0, column=1)


class Plot_Generation_Frame(Sidebar_Frame):
    def __init__(self, root):
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

    def generate_plot(self):
        radius = self.Sidebar.Metric_Frame.entry_radius.get()

        if self.Sidebar.Metric_Frame.validate_radius(radius):
            self.complex = VietorisRipsComplex(
                vertices=self.Main_Window.vertex_coords,
                vertex_names=self.Main_Window.vertex_names,
                radius=radius,
                metric=self.Main_Window.metric)
            
            draw_simplices=not self.Sidebar.Plot_Config_Frame.draw_graph.get()
            self.fig = plot_2d_complex(
                self.complex,
                draw_balls=self.Sidebar.Plot_Config_Frame.draw_balls.get(),
                draw_simplices=draw_simplices
            )

            self.Main_Window.betti = self.complex.get_betti()
    
    def save_plot(self):
        if self.fig == None:
            self.generate_plot()
        else:
            draw_simplices=not self.Sidebar.Plot_Config_Frame.draw_graph.get()
            plot_2d_complex(
                self.complex,
                save_as_file=True,
                draw_balls=self.Sidebar.Plot_Config_Frame.draw_balls.get(),
                draw_simplices=draw_simplices
            )


class Main_Frame(tb.Frame):
    def __init__(self, root, fig, bootstyle='default'):
        tb.Frame.__init__(self, root, bootstyle=bootstyle)

        self.Plot_Frame = Plot_Frame(self, fig)
        self.Plot_Frame.pack(fill='both', expand=True, pady=5)

        self.Betti_Frame = Betti_Frame(self)
        self.Betti_Frame.pack(fill='both', expand=True, pady=5)


class Plot_Frame(tb.Labelframe):
    def __init__(self, root, fig, bootstyle='default'):
        tb.Labelframe.__init__(self, root, text='Plot', bootstyle='default')
        
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side='left', fill='both', expand=True)