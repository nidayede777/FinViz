import tkinter as tk
from tkinter import ttk, messagebox

from mpl_finance import candlestick_ohlc
import matplotlib
matplotlib.use("TkAgg") ##changing backend for matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.animation as anim
from matplotlib import style
import matplotlib.pyplot as plt
style.use("ggplot")

import urllib.request
import json
import pandas as pd
import numpy as np

APP_ICON_PATH = ""
APP_TITLE = "Stock Prices"
APP_GEOMETRY = "1280x800"

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

f = Figure()
a = f.add_subplot(111)
SEARCH_TERM = ""
PLOT = False
COUNTER = 0
DType = 'compact'
PType = 'pl'

DATA = pd.DataFrame()

