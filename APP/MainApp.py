from configration import *
from Views import *


class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.initialize_window()

        self.frames = {}

        for F in (StartPage, SearchPage, PlottingPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        global PLOT
        frame = self.frames[cont]
        if cont == PlottingPage:
            PLOT = True
            frame.update_plot()
        else:
            PLOT = False
        frame.tkraise()

    def initialize_window(self):
        #self.iconbitmap(APP_ICON_PATH)
        self.geometry(APP_GEOMETRY)
        self.title(APP_TITLE)
        self.createMenuBar()
        self.state('zoomed')

    def createMenuBar(self):
        self.menuBar = tk.Menu(self)
        self.createFileMenu()
        self.createPlotModMenu()
        self.config(menu=self.menuBar)

    def createFileMenu(self):
        self.fileMenu = tk.Menu(self.menuBar, tearoff=0)
        self.fileMenu.add_command(label="Save Search")
        self.fileMenu.add_command(label="Open Config")
        self.fileMenu.add_command(label="Quit", command=quit)
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)

    def change_plot_mod(self, what):
        global  DType, PType
        print(DType, PType)
        if what == "length":
            DType = self.len_data.get()
        elif what == "plottype":
            PType = self.plot_type.get()

    def createPlotModMenu(self):
        self.plotModMenu = tk.Menu(self.menuBar, tearoff=0)
        #---------Lehgth of data---------------
        self.len_data = tk.StringVar()
        self.len_data.set("compact")
        self.len_data_menu = tk.Menu(self.plotModMenu, tearoff=0)
        self.len_data_menu.add_radiobutton(label="Compact", value="compact", variable=self.len_data, command=lambda: self.change_plot_mod("length"))
        self.len_data_menu.add_radiobutton(label="Full", value="full", variable=self.len_data, command=lambda: self.change_plot_mod("length"))
        self.plotModMenu.add_cascade(label="Length of Data", menu=self.len_data_menu)

        # ---------Type of Plot---------------
        self.plot_type = tk.StringVar()
        self.plot_type.set("pl")
        self.plot_type_menu = tk.Menu(self.plotModMenu, tearoff=0)
        self.plot_type_menu.add_radiobutton(label="Candelstick Plot", value="cs", variable=self.plot_type,
                                           command=lambda: self.change_plot_mod("plottype"))
        self.plot_type_menu.add_radiobutton(label="Profit Loss Plot", value="pl", variable=self.plot_type,
                                           command=lambda: self.change_plot_mod("plottype"))
        self.plotModMenu.add_cascade(label="Type of Plot", menu=self.plot_type_menu)



        self.plotModMenu.add_command(label="Length of Data")
        self.menuBar.add_cascade(label="Modify Plot", menu=self.plotModMenu)



app = MainApp()
ani1 = anim.FuncAnimation(f, PlottingPage.get_data_thread, interval=1000)
ani2 = anim.FuncAnimation(f, PlottingPage.animate, interval=10000)
app.mainloop()