class gui:
    """
    Purpose:
        Class that contains simple gui interactions
        makes a few buttons and compiles the functions used when buttons are clicked
    Inputs:
        line object from linebuilder, with connected excel_interface
    outputs:
        none, only gui and its object
    Dependencies:
        Tkinter
        excel_interface
        matplotlib
    Example:
        ...
    History:
        Written: Samuel LeBlanc, 2015-08-18, NASA Ames, CA
    """
    def __init__(self,line=None,root=None,noplt=False):
        import Tkinter as tk
        if not line:
            print 'No line_builder object defined'
            return
        self.line = line
        self.flight_num = 0
        self.iactive = 0
        self.colors = ['r']
        self.colorcycle = ['r','b','g','c','m','y']
        if not root:
            self.root = tk.Tk()
        else:
            self.root = root
        self.noplt = noplt
    
    def gui_file_select(self,ext='*',
                        ftype=[('Excel 1997-2003','*.xls'),('Excel','*.xlsx'),
                               ('Kml','*.kml'),('All files','*.*')]):
        """
        Simple gui file select program. Uses TKinter for interface, returns full path
        """
        from Tkinter import Tk
        from tkFileDialog import askopenfilename
        import os
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename(defaultextension=ext,filetypes=ftype) # show an "Open" dialog box and return the path to the selected file
        filename = os.path.abspath(filename)
        return filename

    def gui_file_save(self,ext='*',
                      ftype=[('Excel 1997-2003','*.xls'),('Excel','*.xlsx'),
                             ('Kml','*.kml'),('All files','*.*'),('PNG','*.png')]):
        """
        Simple gui file save select program.
        Uses TKinter for interface, returns full path
        """
        from Tkinter import Tk
        from tkFileDialog import asksaveasfilename
        import os
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        filename = asksaveasfilename(defaultextension=ext,filetypes=ftype) # show an "Open" dialog box and return the path to the selected file
        filename = os.path.abspath(filename)
        return filename

    def make_text(self):
        k = tk.Label(self.root,text='button pressed').pack()
        
    def make_pressed(self):
        self.bpressed.config(relief='sunken')
        
    def gui_saveas2kml(self):
        'Calls the save2kml excel_interface method with new filename'
        if not self.line:
            print 'No line object'
            return
        filename = self.gui_file_save(ext='.kml',ftype=[('All files','*,*'),('KML','*.kml')])
        if not filename: return
        self.kmlfilename = filename
        self.line.ex.save2kml(filename=self.kmlfilename)
        
    def gui_save2kml(self):
        'Calls the save2kml excel_interface method'
        if not self.line:
            print 'No line object'
            return
        if not self.kmlfilename:
            self.stopandquit()
            print 'Problem with kmlfilename'
            return
        self.line.ex.save2kml(filename=self.kmlfilename)

    def gui_save_xl(self):
        'Calls the save2xl excel_interface method'
        if not self.line:
            print 'No line object'
            return
        filename = self.gui_file_save(ext='.xlsx',ftype=[('All files','*.*'),
                                                         ('Excel 1997-2003','*.xls'),
                                                         ('Excel','*.xlsx')])
        if not filename: return
        print 'Saving Excel file to :'+filename
        self.line.ex.save2xl(filename)

    def gui_open_xl(self):
        if not self.line:
            print 'No line object'
            return
        filename = self.gui_file_select(ext='.xls',ftype=[('All files','*.*'),
                                                         ('Excel 1997-2003','*.xls'),
                                                         ('Excel','*.xlsx')])
        if not filename: return
        print 'Opening Excel File:'+filename
        import excel_interface as ex
        self.line.ex = ex.dict_position(filename=filename)
        self.line.onfigureenter([1]) # to force redraw and update from the newly opened excel
        self.line.m.ax.set_title(self.line.ex.datestr)
        self.line.figure.canvas.draw()

    def gui_save2gpx(self):
        'Calls the save2gpx excel_interface method'
        if not self.line:
            print 'No line object'
            return
        filename = self.gui_file_save(ext='.gpx',ftype=[('All files','*.*'),
                                                         ('GPX','*.gpx')])
        if not filename: return
        print 'Saving GPX file to :'+filename
        self.line.ex.save2gpx(filename)
        
    def gui_plotalttime(self):
        'gui function to run the plot of alt vs. time'
        if self.noplt:
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
            from matplotlib.figure import Figure
            import Tkinter as tk
            root = tk.Toplevel()
            root.wm_title('Alt vs. Time')
            fig = Figure()
            canvas = FigureCanvasTkAgg(fig, master=root)
            canvas.show()
            canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            tb = NavigationToolbar2TkAgg(canvas,root)
            tb.pack(side=tk.BOTTOM)
            tb.update()
            canvas._tkcanvas.pack(side=tk.TOP,fill=tk.BOTH,expand=1)
            ax1 = fig.add_subplot(111)
        else:
            import matplotlib.pyplot as plt
            f1 = plt.gcf()
            fig = plt.figure()
            ax1 = fig.add_subplot(1)
        ax1.plot(self.line.ex.cumlegt,self.line.ex.alt,'x-')
        ax1.set_xlabel('Flight duration [Hours]')
        ax1.set_ylabel('Alt [km]')
        ax1.xaxis.tick_bottom()
        ax2 = ax1.twiny()
        ax2.xaxis.tick_top()
        ax2.set_xlabel('UTC [Hours]')
        ax2.set_xticks(self.line.ex.cumlegt)
        ax2.set_xticklabels(self.line.ex.utc)
        if self.noplt:
            canvas.draw()
        else:
            plt.figure(f1.number)

    def gui_newflight(self):
        'Program to call and create a new excel spreadsheet'
        import tkSimpleDialog
        import excel_interface as ex
        import Tkinter as tk
        print 'Not yet'
        return
        
        newname = tkSimpleDialog.askstring('New flight path',
                                           'New flight path name:')
        if not newname:
            print 'Cancelled'
            return
        self.flight_num = self.flight_num+1
        self.colors.append(self.colorcycle[self.flight_num])
        self.flightselect_arr.append(tk.Radiobutton(self.root,text=newname,
                                                    variable=self.iactive,
                                                    value=self.flight_num,
                                                    indicatoron=0,
                                                    command=self.gui_changeflight))
        self.flightselect_arr[self.flight_num].pack(in_=self.frame_select,side=tk.BOTTOM,
                                                    padx=2,pady=2,fill=tk.BOTH)
        self.line.ex_arr.append(ex.dict_position(datestr=self.line.ex.datestr,
                                                 name=newname,
                                                 newsheetonly=True,
                                                 sheet_num=self.flight_num))
        self.line.newline()
        self.iactive = self.flight_num
        self.gui_changeflight()
        

    def gui_changeflight(self):
        'method to switch out the active flight path that is used'
        self.flightselect_arr[self.iactive].select()
        self.line.iactive = self.iactive
        self.line.ex = self.line.ex_arr[self.iactive]
        self.line.makegrey()
        self.line.line = self.line.line_arr[self.iactive]
        self.line.ex.switchsheet(self.iactive)
        self.line.colorme(self.colors[self.iactive])
        
    def gui_savefig(self):
        'gui program to save the current figure as png'
        if not self.line:
            print 'No line object'
            return
        filename = self.gui_file_save(ext='.png')
        if not filename: return
        import matplotlib as plt
        plt.savefig(filename,dpi=600,transparent=True)

    def stopandquit(self):
        'function to force a stop and quit the mainloop, future with exit of python'
        self.root.quit()
        self.root.destroy()
        import sys
        #sys.exit()
    
    def make_gui(self):
        """
        make the gui with buttons
        """
        import Tkinter as tk
        self.bopenfile = tk.Button(self.root,text='Open Excel file',
                                   command=self.gui_open_xl)
        self.bsavexl = tk.Button(self.root,text='Save Excel file',
                                 command=self.gui_save_xl)
        self.bsaveas2kml = tk.Button(self.root,text='SaveAs to Kml',
                                   command=self.gui_saveas2kml)
        self.bsave2kml = tk.Button(self.root,text='Update Kml',
                                   command=self.gui_save2kml)
        #self.bsavefig = tk.Button(self.root,text='Save as png',
        #                              command=self.gui_savefig)
        #bmaketext = tk.Button(text='text',command=make_text)
        #bpressed = tk.Button(text='button on',command=make_pressed)
        self.bopenfile.pack()
        self.bsavexl.pack()
        self.bsaveas2kml.pack()
        self.bsave2kml.pack()
        #self.bsavefig.pack()
        tk.Frame(self.root,height=2,width=100,bg='black',relief='sunken').pack(padx=5,pady=5)
        tk.Label(self.root,text='--- Options ---').pack()
        if self.line:
            self.yup = True
            #self.bshowWP = tk.Button(self.root,text='Show Waypoints',
            #                         command=self.bshowpressed)
            self.bplotalt = tk.Button(self.root,text='Plot alt vs time',
                                      command=self.gui_plotalttime)
            self.bplotalt.pack()

        tk.Frame(self.root,height=2,width=100,bg='black',relief='sunken').pack(padx=5,pady=5)    
        tk.Button(self.root,text='Quit',command=self.stopandquit).pack()
        #bpressed.pack()
        #bmaketext.pack()
        self.root.mainloop()

