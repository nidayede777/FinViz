from configration import *
import threading

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.label = ttk.Label(self, text="Welcome to my Trading App. Agree the TC to proceed!", font=LARGE_FONT)
        self.label.pack(padx=10, pady=10)

        self.button1 = ttk.Button(self, text="Agree", command=lambda: controller.show_frame(SearchPage))
        self.button1.pack()

        self.button2 = ttk.Button(self, text="Disagree", command=quit)
        self.button2.pack()



class SearchPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.label = ttk.Label(self,
                               text="Search the name of the company and get interactive visualization of the stock data",
                               font=LARGE_FONT)
        self.label.pack(padx=10, pady=10)

        label1 = ttk.Label(self, text="Company Name/Stock ID", font=NORM_FONT)
        self.searchTerm = tk.StringVar()
        self.searchBox = ttk.Entry(self, textvariable=self.searchTerm, width=50)
        self.sch = ttk.Button(self, text="Search", command=self.search)
        self.Lb1 = tk.Listbox(self, width=50, state=tk.DISABLED)
        self.sub = ttk.Button(self, text="Submit", state=tk.DISABLED, command=lambda: self.submit(controller))

        label1.pack(padx=10, pady=10)
        self.searchBox.pack(padx=10, pady=10)
        self.sch.pack(padx=10, pady=10)
        self.Lb1.pack(padx=10, pady=10)
        self.sub.pack(padx=10, pady=10)

        self.searchBox.bind('<Return>', self.search)

    def search(self, event=None):
        search_link = "https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords="
        api_key="&apikey=GR8RTDRZ1Y1R0MRT"
        kw = self.searchTerm.get()
        search_link = search_link + kw + api_key
        self.Lb1.delete(0, tk.END)

        try:
            with urllib.request.urlopen(search_link) as url:
                data = json.loads(url.read().decode())
                data = data["bestMatches"]
                data = pd.DataFrame(data)
            dim = data.shape
            names = data["2. name"]
            smbls = data["1. symbol"]
            currs = data["8. currency"]
            self.sub['state'] = 'normal'
            self.Lb1['state'] = 'normal'
            for i in range(dim[0]):
                self.Lb1.insert(i, "{3} : ({0}), {1}, {2}".format(smbls[i], names[i], currs[i], i))
            self.Lb1.selection_set(0)
        except:
            msg = "Sorry! No results found for {0}".format(kw)
            self.show_error(msg)

    def submit(self, controller):
        global SEARCH_TERM, PLOT
        s = self.Lb1.get(self.Lb1.curselection())
        print(s)
        i1 = s.find("(")
        i2 = s.find(")")
        symbl = s[i1+1:i2]
        print(symbl)
        SEARCH_TERM = symbl
        PLOT = True
        controller.show_frame(PlottingPage)

    def show_error(self, msg):
        messagebox.showwarning("Error", msg)


class PlottingPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.var = tk.StringVar(value="")
        label = ttk.Label(self, textvariable=self.var, font=LARGE_FONT)
        label.pack(padx=10, pady=10)
        self.button1 = ttk.Button(self, text="Search", command=lambda: controller.show_frame(SearchPage))
        self.button1.pack()

        # plot in backend
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()  # insted of .show use .draw now
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def update_plot(self):
        value = "Symbol : " + SEARCH_TERM
        self.var.set(value)

    @staticmethod
    def get_data():
        global SEARCH_TERM, DATA, DType, PType
        print(DType, PType)
        try:
            dl1 = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="
            dl2 = "&outputsize=compact&apikey=GR8RTDRZ1Y1R0MRT"
            dataLink = dl1 + SEARCH_TERM + dl2
            with urllib.request.urlopen(
                    dataLink) as url:
                data = json.loads(url.read().decode())
                data = data["Time Series (Daily)"]
            data = pd.DataFrame(data)
            DATA = data.T
            print("Success, getting Data")
        except:
            print("Unable to read data for : ", SEARCH_TERM)

    @staticmethod
    def get_data_thread(i):
        global COUNTER, PLOT, DATA
        if PLOT:
            if COUNTER == 10:
                COUNTER = 0
                t = threading.Thread(target=PlottingPage.get_data, name="Thread 1")
                t.start()
            COUNTER += 1
        else:
            COUNTER = 10
            if not DATA.empty:
                DATA = pd.DataFrame()

    @staticmethod
    def animate(i=None):
        global SEARCH_TERM, a, f, DATA, DType, PType
        if not DATA.empty:
            print("Success, Plotting : ", SEARCH_TERM)

            #----------Creating a candelstick graph--------
            if PType == "cs":
                dates = np.array(DATA.index.tolist()).astype(np.datetime64)
                open = DATA["1. open"]
                high = DATA["2. high"]
                low = DATA["3. low"]
                close = DATA["4. close"]
                volume = DATA["5. volume"]
                dates = [mdates.date2num(d) for d in dates]

                ohlc = []
                for i in range(len(dates)):
                    append_me = dates[i], float(open[i]), float(high[i]), float(low[i]), float(close[i]), float(volume[i])
                    ohlc.append(append_me)

                a.clear()
                candlestick_ohlc(a, ohlc, width=0.4)  # , colorup='#77d879', colordown='#db3f3f')

                for label in a.xaxis.get_ticklabels():
                    label.set_rotation(45)

                a.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
                a.xaxis.set_major_locator(mticker.MaxNLocator(10))
                a.set_title("Daily stock price\nLast Price : " + str(close[-1]))
                #---------------END Candelstick PART-----------------

                # ----------Creating a Profit Loss graph--------
            elif PType == "pl":
                dates = np.array(DATA.index.tolist()).astype("datetime64[s]")
                close = np.array(DATA["4. close"]).astype(float)
                open = np.array(DATA["1. open"]).astype(float)
                ch = close.sum() / (len(close))
                a.clear()
                a.plot_date(dates, open, '#00A3E0', label="Open")
                a.plot_date(dates, close, '#183A54', label="Close")
                a.fill_between(dates, close, ch, where=(close>ch), facecolor='g', alpha=0.3)
                a.fill_between(dates, close, ch, where=(close<ch), facecolor='r', alpha=0.3)
                a.plot([], [], linewidth=5, label="Loss", color='r', alpha=0.3)
                a.plot([], [], linewidth=5, label="Profit", color='g', alpha=0.3)
                for label in a.xaxis.get_ticklabels():
                    label.set_rotation(45)
                a.legend(bbox_to_anchor=(0, 1.02, 1, 0.102), loc=3, ncol=2, borderaxespad=0)
                a.set_title("Daily stock price\nLast Price : " + str(close[-1]))
                # ----------End Profit Loss graph--------
        else:
            print("No data to plot for : ", SEARCH_TERM)