import matplotlib
import os
fp = os.path.dirname(os.path.abspath(__file__))
matplotlib.rc_file(fp+os.path.sep+'file.rc')
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import Tkinter as tk
import numpy as np
from mpl_toolkits.basemap import Basemap
import sys
import map_utils as mu
import excel_interface as ex
import map_interactive as mi
import gui

def Create_gui():
    'Program to set up gui interaction with figure embedded'
    import tkSimpleDialog
    class ui:
        pass
    ui = ui
    ui.root = tk.Tk()
    ui.root.wm_title('Flight planning - map by Samuel LeBlanc, NASA Ames')
    ui.root.geometry('900x950')
    ui.top = tk.Frame(ui.root)
    ui.bot = tk.Frame(ui.root)
    ui.top.pack(side=tk.TOP,expand=False)
    ui.bot.pack(side=tk.BOTTOM,fill=tk.BOTH,expand=True)
    ui.fig = Figure()
    ui.ax1 = ui.fig.add_subplot(111)
    ui.canvas = FigureCanvasTkAgg(ui.fig,master=ui.root)
    ui.canvas.show()
    ui.canvas.get_tk_widget().pack(in_=ui.bot,side=tk.BOTTOM,fill=tk.BOTH,expand=1)
    ui.tb = NavigationToolbar2TkAgg(ui.canvas,ui.root)
    ui.tb.pack(in_=ui.bot,side=tk.BOTTOM)
    ui.tb.update()
    ui.canvas._tkcanvas.pack(in_=ui.bot,side=tk.TOP,fill=tk.BOTH,expand=1)
    ui.date = tkSimpleDialog.askstring('Flight Date','Flight Date (yyyy-mm-dd):')
    ui.ax1.set_title(ui.date)
    return ui

def build_buttons(ui,lines):
    'Program to set up the buttons'
    import gui
    import Tkinter as tk
    g = gui.gui(lines,root=ui.root,noplt=True)
    g.bopenfile = tk.Button(g.root,text='Open Excel file',
                            command=g.gui_open_xl)
    g.bsavexl = tk.Button(g.root,text='Save Excel file',
                          command=g.gui_save_xl)
    g.bsaveas2kml = tk.Button(g.root,text='SaveAs to Kml',
                              command=g.gui_saveas2kml)
    g.bsave2kml = tk.Button(g.root,text='Update Kml',
                            command=g.gui_save2kml)
    g.bopenfile.pack(in_=ui.top,side=tk.LEFT)
    g.bsavexl.pack(in_=ui.top,side=tk.LEFT)
    g.bsaveas2kml.pack(in_=ui.top,side=tk.LEFT)
    g.bsave2kml.pack(in_=ui.top,side=tk.LEFT)
    tk.Frame(g.root,height=20,width=2,bg='black',relief='sunken'
             ).pack(in_=ui.top,side=tk.LEFT,padx=8,pady=5)
    g.bplotalt = tk.Button(g.root,text='Plot alt vs time',
                           command=g.gui_plotalttime)
    g.bplotalt.pack(in_=ui.top,side=tk.LEFT)
    tk.Frame(g.root,height=20,width=2,bg='black',relief='sunken'
             ).pack(in_=ui.top,side=tk.LEFT,padx=8,pady=5)
    tk.Button(g.root,text='Quit',command=g.stopandquit).pack(in_=ui.top,side=tk.LEFT)

def Create_interaction(**kwargs):
    ui = Create_gui()
    m = mi.build_basemap(ax=ui.ax1)
    
    lat0,lon0 = mi.pll('22 58.783S'), mi.pll('14 38.717E')
    x0,y0 = m(lon0,lat0)
    line, = m.plot([x0],[y0],'ro-')
    text = ('Press s to stop interaction\\n'
            'Press i to restart interaction\\n')
    wb = ex.dict_position(**kwargs)
    lines = mi.LineBuilder(line,m=m,ex=wb,tb=ui.tb)
    
    build_buttons(ui,lines)

    ui.root.mainloop()
    return lines

if __name__ == "__main__":
    lines = Create_interaction()
