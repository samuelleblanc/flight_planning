#import matplotlib
#import os,sys
#fp = os.path.dirname(os.path.abspath(__file__))
#matplotlib.rc_file(fp+os.path.sep+'file.rc')
#matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import Tkinter as tk
import numpy as np
from mpl_toolkits.basemap import Basemap
import datetime

import map_utils as mu
import excel_interface as ex
import map_interactive as mi
import gui

version = 'v0.3'

def Create_gui(vertical=True):
    'Program to set up gui interaction with figure embedded'
    class ui:
        pass
    ui = ui
    ui.root = tk.Tk()
    ui.root.wm_title('Flight planning by Samuel LeBlanc, NASA Ames, '+version)
    ui.root.geometry('900x950')
    ui.top = tk.Frame(ui.root)
    ui.bot = tk.Frame(ui.root)
    if vertical:
        ui.top.pack(side=tk.LEFT,expand=False)
        ui.bot.pack(side=tk.RIGHT,fill=tk.BOTH,expand=True)
    else:
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
    return ui

def build_buttons(ui,lines,vertical=True):
    'Program to set up the buttons'
    import gui
    import Tkinter as tk
    if vertical:
        side = tk.TOP
        h = 2
        w = 20
    else:
        side = tk.LEFT
        h = 20
        w = 2
    g = gui.gui(lines,root=ui.root,noplt=True)
    g.refresh = tk.Button(g.root,text='Refresh',
                          command=g.refresh,
                          bg='chartreuse')
    g.bopenfile = tk.Button(g.root,text='Open Excel file',
                            command=g.gui_open_xl)
    g.bsavexl = tk.Button(g.root,text='Save Excel file',
                          command=g.gui_save_xl)
    g.bsaveas2kml = tk.Button(g.root,text='SaveAs to Kml',
                              command=g.gui_saveas2kml)
    g.bsave2kml = tk.Button(g.root,text='Update Kml',
                            command=g.gui_save2kml)
    g.bsave2gpx = tk.Button(g.root,text='Save to GPX',
                            command=g.gui_save2gpx)
    g.refresh.pack(in_=ui.top,side=side,fill=tk.X,pady=8)
    g.bopenfile.pack(in_=ui.top,side=side)
    g.bsavexl.pack(in_=ui.top,side=side)
    g.bsaveas2kml.pack(in_=ui.top,side=side)
    g.bsave2kml.pack(in_=ui.top,side=side)
    g.bsave2gpx.pack(in_=ui.top,side=side)
    tk.Frame(g.root,height=h,width=w,bg='black',relief='sunken'
             ).pack(in_=ui.top,side=side,padx=8,pady=5)
    g.bplotalt = tk.Button(g.root,text='Plot alt vs time',
                           command=g.gui_plotalttime)
    g.bplotalt.pack(in_=ui.top,side=side)
    tk.Frame(g.root,height=h,width=w,bg='black',relief='sunken'
             ).pack(in_=ui.top,side=side,padx=8,pady=5)
    g.frame_select = tk.Frame(g.root,relief=tk.SUNKEN,bg='white')
    g.frame_select.pack(in_=ui.top,side=side,fill=tk.BOTH)
    g.flightselect_arr = []
    g.flightselect_arr.append(tk.Radiobutton(g.root,text=lines.ex.name,
                                             variable=g.iactive,value=0,
                                             indicatoron=0,
                                             command=g.gui_changeflight,
                                             state=tk.ACTIVE))
    g.flightselect_arr[0].pack(in_=g.frame_select,side=side,padx=4,pady=2,fill=tk.BOTH)
    g.flightselect_arr[0].select()
    g.newflightpath = tk.Button(g.root,text='New flight path',
                                command = g.gui_newflight)
    g.newflightpath.pack(in_=ui.top,padx=5,pady=5)
    tk.Frame(g.root,height=h,width=w,bg='black',relief='sunken'
             ).pack(in_=ui.top,side=side,padx=8,pady=5)
    tk.Button(g.root,text='Quit',command=g.stopandquit,bg='lightcoral'
              ).pack(in_=ui.top,side=side)

def get_datestr(ui):
    import tkSimpleDialog
    import datetime
    ui.datestr = tkSimpleDialog.askstring('Flight Date','Flight Date (yyyy-mm-dd):')
    if not ui.datestr:
        ui.datestr = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    ui.ax1.set_title(ui.datestr)

def savetmp(ui,wb):
    import tempfile, os
    tmpfilename = os.path.join(tempfile.gettempdir(),ui.datestr+'.xlsx')
    try:
        wb.save2xl(tmpfilename)
    except:
        print 'unable to save excel to temp file:'+tmpfilename
        print 'continuing ...'

def init_plot(m):
    lat0,lon0 = mi.pll('22 58.783S'), mi.pll('14 38.717E')
    x0,y0 = m(lon0,lat0)
    line, = m.plot([x0],[y0],'ro-')
    text = ('Press s to stop interaction\\n'
            'Press i to restart interaction\\n')
    return line

def Create_interaction(**kwargs):
    ui = Create_gui()

    m = mi.build_basemap(ax=ui.ax1)
    line = init_plot(m)

    get_datestr(ui)
    wb = ex.dict_position(datestr=ui.datestr,**kwargs)
    lines = mi.LineBuilder(line,m=m,ex=wb,tb=ui.tb)
    savetmp(ui,wb)
    
    build_buttons(ui,lines)    
    ui.root.mainloop()
    return lines

if __name__ == "__main__":
    lines = Create_interaction()
