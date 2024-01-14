import ttkbootstrap as tb

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