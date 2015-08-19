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
    Example:
        ...
    History:
        Written: Samuel LeBlanc, 2015-08-18, NASA Ames, CA
    """
    def __init__(self,line=None):
        import Tkinter as tk
        if not line:
            print 'No line_builder object defined'
            return
        self.line = line
        self.root = tk.Tk()
    
    def gui_file_select(self,ext='*'):
        """
        Simple gui file select program. Uses TKinter for interface, returns full path
        """
        from Tkinter import Tk
        from tkFileDialog import askopenfilename
        ftype=[('Excel 1997-2003','*.xls'),
               ('Excel','*.xlsx'),
               ('Kml','*.kml'),
               ('All files','*.*')]
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename(defaultextension=ext,filetypes=ftype) # show an "Open" dialog box and return the path to the selected file
        return filename

    def gui_file_save(self,ext='*'):
        """
        Simple gui file save select program.
        Uses TKinter for interface, returns full path
        """
        from Tkinter import Tk
        from tkFileDialog import asksaveasfilename
        ftype=[('Excel 1997-2003','*.xls'),
               ('Excel','*.xlsx'),
               ('Kml','*.kml'),
               ('All files','*.*'),
               ('PNG','*.png')]

        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        filename = asksaveasfilename(defaultextension=ext,filetypes=ftype) # show an "Open" dialog box and return the path to the selected file
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
        filename = self.gui_file_save(ext='.kml')
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
        filename = self.gui_file_save(ext='.xlsx')
        if not filename: return
        self.line.ex.save2xl()

    def gui_open_xl(self):
        if not self.line:
            print 'No line object'
            return
        filename = self.gui_file_select(ext='.xls')
        if not filename: return
        import excel_interface as ex
        self.line.ex = ex.dict_position(filename=filename)
        self.line.onfigureenter([1]) # to force redraw and update from the newly opened excel

    def gui_plotalttime(self):
        'gui function to run the plot of alt vs. time'
        print 'Not yet implemented'

    def gui_savefig(self):
        'gui program to save the current figure as png'
        filename = self.gui_file_save(ext='.png')
        if not filename: return
        if not line:
            print 'No line to save'
            return
        line.m.savefig(filename,dpi=600,transparent=True)

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
        self.bsavefig = tk.Button(self.root,text='Save as png',
                                      command=self.gui_savefig)
        #bmaketext = tk.Button(text='text',command=make_text)
        #bpressed = tk.Button(text='button on',command=make_pressed)
        self.bopenfile.pack()
        self.bsavexl.pack()
        self.bsaveas2kml.pack()
        self.bsave2kml.pack()
        self.bsavefig.pack()
        tk.Text(self.root,text='--- Options ---').pack()
        if self.line:
            self.yup = True
            #self.bshowWP = tk.Button(self.root,text='Show Waypoints',
            #                         command=self.bshowpressed)
            self.bplotalt = tk.Button(self.root,text='Plot alt vs time',
                                      command=self.gui_plotalttime)
            self.bplotalt.pack()
            
        tk.Text(self.root,text='---------------').pack()
        tk.Button(self.root,text='Quit',command=self.stopandquit).pack()
        #bpressed.pack()
        #bmaketext.pack()
        self.root.mainloop()

