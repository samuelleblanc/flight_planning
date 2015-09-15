import tkSimpleDialog

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
        os.path
        matplotlib
        tkFileDialog
    Example:
        ...
    History:
        Written: Samuel LeBlanc, 2015-08-18, NASA Ames, CA
        Modified: Samuel LeBlanc, 2015-09-02, Santa Cruz, CA
	          - added handlers for a few new buttons
		  - modified imports to be more specific
        Modified: Samuel LeBlanc, 2015-09-10, Santa Cruz, CA
	          - adding new flight path for another plane capabilities
    """
    def __init__(self,line=None,root=None,noplt=False):
        import Tkinter as tk
        if not line:
            print 'No line_builder object defined'
            return
        self.line = line
        self.flight_num = 0
        self.iactive = tk.IntVar()
	self.iactive.set(0)
        self.colors = ['red']
        self.colorcycle = ['red','blue','green','cyan','magenta','yellow','black','white']
        if not root:
            self.root = tk.Tk()
        else:
            self.root = root
        self.noplt = noplt
	self.newflight_off = True
    
    def gui_file_select(self,ext='*',
                        ftype=[('Excel 1997-2003','*.xls'),('Excel','*.xlsx'),
                               ('Kml','*.kml'),('All files','*.*')]):
        """
        Simple gui file select program. Uses TKinter for interface, returns full path
        """
        from Tkinter import Tk
        from tkFileDialog import askopenfilename
        from os.path import abspath
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        filename = askopenfilename(defaultextension=ext,filetypes=ftype) # show an "Open" dialog box and return the path to the selected file
        if filename:
	    filename = abspath(filename)
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
        from os.path import abspath
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        filename = asksaveasfilename(defaultextension=ext,filetypes=ftype) # show an "Open" dialog box and return the path to the selected file
        filename = abspath(filename)
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

    def gui_save_txt(self):
        'Calls the save2txt excel_interface method'
        if not self.line:
            print 'No line object'
            return
	import tkMessageBox
        tkMessageBox.showwarning('Saving one flight','Saving flight path of:%s' %self.line.ex.name)
	filename = self.gui_file_save(ext='.txt',ftype=[('All files','*.*'),
                                                         ('Plain text','*.txt')])
        if not filename: return
        print 'Saving Text file to :'+filename
        self.line.ex.save2txt(filename)

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
        self.line.disconnect()
        self.line.ex.wb.close()
        self.line.tb.set_message('Opening Excel File:'+filename)
        import excel_interface as ex
        self.flight_num = 0
        self.iactive.set(0)
        self.line.ex_arr = ex.populate_ex_arr(filename=filename,colorcycle=self.colorcycle)
        self.line.m.ax.set_title(self.line.ex_arr[0].datestr)
        for b in self.flightselect_arr:
            b.destroy()
        self.flightselect_arr = []
        try:
            self.line.m.figure_under.remove()
        except:
            pass
        try:
            for s in self.sat_obj:
                s.remove()
        except:
            pass
        self.colors = []
        for i in range(len(self.line.ex_arr)):
	    self.line.ex = self.line.ex_arr[i]
	    self.line.onfigureenter([1]) # to force redraw and update from the newly opened excel
            self.load_flight(self.line.ex)
        self.line.line.figure.canvas.draw()
        self.line.connect()

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
            print 'Problem with loading a new figure handler'
            return
        ax1.plot(self.line.ex.cumlegt,self.line.ex.alt,'x-')
        ax1.set_title('Altitude vs time for %s' % self.line.ex.datestr,y=1.08)
	fig.subplots_adjust(top=0.85,right=0.8)
	ax1.set_xlabel('Flight duration [Hours]')
        ax1.set_ylabel('Alt [m]')
        ax1.xaxis.tick_bottom()
        ax2 = ax1.twiny()
        ax2.xaxis.tick_top()
        ax2.set_xlabel('UTC [Hours]')
        ax2.set_xticks(ax1.get_xticks())
	cum2utc = self.line.ex.utc[0]
	utc_label = ['%2.2f'%(u+cum2utc) for u in ax1.get_xticks()]
	ax2.set_xticklabels(utc_label)
	ax3 = ax1.twinx()
	ax3.yaxis.tick_right()
	ax3.set_ylabel('Altitude [Kft]')
	ax3.set_yticks(ax1.get_yticks())
	alt_labels = ['%2.2f'%(a*3.28084/1000.0) for a in ax1.get_yticks()]
	ax3.set_yticklabels(alt_labels)
	ax1.grid()
        if self.noplt:
            canvas.draw()
        else:
            plt.figure(f1.number)

    def gui_plotsza(self):
        'gui function to plot the solar zenith angle of the flight path'
	#import tkMessageBox
	#tkMessageBox.showwarning('Sorry','Feature not yet implemented') 
	#return 
	if not self.noplt:
	     print 'No figure handler, sorry will not work'
	     return
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
	ax1 = fig.add_subplot(2,1,1)
	ax1.plot(self.line.ex.cumlegt,self.line.ex.sza,'x-')
	ax1.set_title('Solar position along flight track for %s' % self.line.ex.datestr, y=1.18)
	fig.subplots_adjust(top=0.85)
	#ax1.set_xlabel('Flight duration [Hours]')
	ax1.set_ylabel('SZA [degree]')
	#ax1.set_xticklabels(['','','','','',''])
	ax1.grid()
	axticks = ax1.get_xticks()
	ax1_up = ax1.twiny()
	ax1_up.xaxis.tick_top()
	cum2utc = self.line.ex.utc[0]
	ax1_up.set_xticks(axticks)
	utc_label = ['%2.2f'%(u+cum2utc) for u in axticks]
	ax1_up.set_xticklabels(utc_label)
	ax1_up.set_xlabel('UTC [Hours]')
	ax2 = fig.add_subplot(2,1,2,sharex=ax1)
	ax2.plot(self.line.ex.cumlegt,self.line.ex.azi,'o')
	ax2.set_ylabel('AZI [degree]')
	ax2.set_xlabel('Flight duration [Hours]')
	ax2.grid()
	canvas.draw()

    def load_flight(self,ex):
        'Program to populate the arrays of multiple flights with the info of one array'
	import Tkinter as tk
	self.colors.append(ex.color)
	self.line.tb.set_message('load_flight values for:%s' %ex.name)

        self.flightselect_arr.append(tk.Radiobutton(self.root,text=ex.name,
                                                    fg=ex.color,
                                                    variable=self.iactive,
                                                    value=self.flight_num,
                                                    indicatoron=0,
                                                    command=self.gui_changeflight,bg='white'))
        self.flightselect_arr[self.flight_num].pack(in_=self.frame_select,side=tk.TOP,
                                                    padx=4,pady=2,fill=tk.BOTH)
        self.line.newline()
        self.iactive.set(self.flight_num)
        self.gui_changeflight()
        self.flight_num = self.flight_num+1

    def gui_newflight(self):
        'Program to call and create a new excel spreadsheet'
        import tkSimpleDialog,tkMessageBox
        import excel_interface as ex
        import Tkinter as tk
        if self.newflight_off:
	     tkMessageBox.showwarning('Sorry','Feature not yet implemented')
             return
        
        newname = tkSimpleDialog.askstring('New flight path',
                                           'New flight path name:')
        if not newname:
            print 'Cancelled'
            return
        self.flight_num = self.flight_num+1
        self.colors.append(self.colorcycle[self.flight_num])
        self.flightselect_arr.append(tk.Radiobutton(self.root,text=newname,
	                                            fg=self.colorcycle[self.flight_num],
                                                    variable=self.iactive,
                                                    value=self.flight_num,
                                                    indicatoron=0,
                                                    command=self.gui_changeflight,bg='white'))
        self.flightselect_arr[self.flight_num].pack(in_=self.frame_select,side=tk.TOP,
                                                    padx=4,pady=2,fill=tk.BOTH)
        self.line.ex_arr.append(ex.dict_position(datestr=self.line.ex.datestr,
                                                 name=newname,
                                                 newsheetonly=True,
                                                 sheet_num=self.flight_num,
                                                 color=self.colorcycle[self.flight_num]))
        self.line.newline()
        self.iactive.set(self.flight_num)
        self.gui_changeflight()

    def gui_removeflight(self):
        'Program to call and remove a flight path from the plotting'
        import tkSimpleDialog,tkMessageBox
        tkMessageBox.showwarning('Sorry','Feature not yet implemented')
        return
        import excel_interface as ex
        import Tkinter as tk
        from gui import Select_flights
        self.name_arr = []
        for x in self.line.ex_arr:
            self.name_arr.append(x)
        flights = Select_flights(self.name_arr,title='Delete Flights',Text='Choose flights to delete')
        for i,val in enumerate(flights.result):
            if val:
                name2del = self.line.ex_arr[i].name
                self.flightselect_arr[i].destroy()
                for i in range(i,len(self.flightselect_arr)):
                    self.flightselect_arr[i].configure({'value':i-1})
                self.flightselect_arr[i].remove()
                self.line.removeline(i)
                self.line.ex_arr[i].exremove()
                self.line.ex_arr[i].remove()
    
    def gui_changeflight(self):
        'method to switch out the active flight path that is used'
	if self.newflight_off:
	     import tkMessageBox
	     tkMessageBox.showwarning('Sorry','Feature not yet implemented')
	     return
	self.flightselect_arr[self.iactive.get()].select()
        self.line.iactive = self.iactive.get()
        self.line.ex = self.line.ex_arr[self.iactive.get()]
        self.line.makegrey()
        self.line.line = self.line.line_arr[self.iactive.get()]
        self.line.ex.switchsheet(self.iactive.get())
        self.line.colorme(self.colors[self.iactive.get()])
        
    def gui_savefig(self):
        'gui program to save the current figure as png'
        if not self.line:
            print 'No line object'
            return
        filename = self.gui_file_save(ext='.png')
        if not filename: return
        print 'Use toolbar'

    def stopandquit(self):
        'function to force a stop and quit the mainloop, future with exit of python'
        self.root.quit()
        self.root.destroy()
        self.line.ex.wb.close()
        #import sys
        #sys.exit()

    def refresh(self):
        'function to force a refresh of the plotting window'
        self.line.onfigureenter([1])
        
    
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

    def gui_addpoint(self):
        'Gui button to add a point via a dialog'
        from gui import Move_point
        m = Move_point()
        self.line.newpoint(m.bear,m.dist)

    def gui_movepoints(self):
        'GUI button to move many points at once'
        from gui import Select_flights,Move_point
        wp_arr = []
        for w in self.line.ex.WP:
            wp_arr.append('WP #%i'%w)
        p = Select_flights(wp_arr,title='Move points',Text='Select points to move:')
        m = Move_point()
        for i,val in enumerate(p.result):
            if val:
                self.line.movepoint(i,m.bear,m.dist)

    def gui_addsat(self):
        'Gui button to add the satellite tracks'
        from tkMessageBox import askquestion
        answer = askquestion('Verify import satellite tracks','Do you want to get the satellite tracks from the internet?')
        if answer == 'yes':
            from map_interactive import load_sat_from_net, get_sat_tracks, plot_sat_tracks
            self.line.tb.set_message('Loading satellite kml File from internet')
            kml = load_sat_from_net()
            if kml:
                self.line.tb.set_message('parsing file...')
                sat = get_sat_tracks(self.line.ex.datestr,kml)
                self.line.tb.set_message('Plotting satellite tracks')
                self.sat_obj = plot_sat_tracks(self.line.m,sat)
        elif answer ==  'no':
            from map_interactive import load_sat_from_file, get_sat_tracks, plot_sat_tracks
            filename = self.gui_file_select(ext='.kml',ftype=[('All files','*.*'),
                                                         ('Google Earth','*.kml')])
            if not filename:
                print 'Cancelled, no file selected'
                return
            self.line.tb.set_message('Opening kml File:'+filename)
            kml = load_sat_from_file(filename)
            self.line.tb.set_message('parsing file...')
            sat = get_sat_tracks(self.line.ex.datestr,kml)
            self.line.tb.set_message('Plotting satellite tracks') 
            self.sat_obj = plot_sat_tracks(self.line.m,sat)

    def gui_addbocachica(self):
        'GUI handler for adding bocachica foreacast maps to basemap plot'
	import tkMessageBox
	from scipy.misc import imread
	#tkMessageBox.showwarning('Sorry','Feature not yet implemented')
	#return
	filename = self.gui_file_select(ext='.png',ftype=[('All files','*.*'),
                                                          ('PNG','*.png')])
        if not filename:
            print 'Cancelled, no file selected'
            return
        print 'Opening png File:'+filename
	img = imread(filename)
        ll_lat,ll_lon,ur_lat,ur_lon = -40.0,-30.0,10.0,40.0
        self.line.addfigure_under(img[42:674,50:1015,:],ll_lat,ll_lon,ur_lat,ur_lon)
	#self.line.addfigure_under(img[710:795,35:535,:],ll_lat-7.0,ll_lon,ll_lat-5.0,ur_lon-10.0,outside=True)


    def gui_addfigure(self,ll_lat=None,ll_lon=None,ur_lat=None,ur_lon=None):
        'GUI handler for adding figures forecast maps to basemap plot'
        from scipy.misc import imread
	import PIL
        import tkMessageBox, tkSimpleDialog
        #tkMessageBox.showwarning('Sorry','Feature in beta')
        #return
        filename = self.gui_file_select(ext='.png',ftype=[('All files','*.*'),
                                                          ('PNG','*.png'),
							  ('JPEG','*.jpg'),
							  ('GIF','*.gif')])
        if not filename:
            print 'Cancelled, no file selected'
            return
        print 'Opening png File: %s' %filename
	img = imread(filename)
	
	# get the corners
	if not ll_lat:
	    ll_lat = tkSimpleDialog.askfloat('Lower left lat','Lower left lat? [deg]')
	    ll_lon = tkSimpleDialog.askfloat('Lower left lon','Lower left lon? [deg]')
	    ur_lat = tkSimpleDialog.askfloat('Upper right lat','Upper right lat? [deg]')
	    ur_lon = tkSimpleDialog.askfloat('Upper right lon','Upper right lon? [deg]')

	self.line.addfigure_under(img,ll_lat,ll_lon,ur_lat,ur_lon,alpha=0.6)

class Select_flights(tkSimpleDialog.Dialog):
    """
    Purpose:
        Dialog box that loads a list of points or flights to be selected.
    Inputs:
        tkSimple.Dialog
        pt_list: list of string array in the correct positions
        title: title of dialog window
        text: text to be displayed before the checkbox selection
    Outputs:
        list of integers that are selected
    Dependencies:
        tkSimpleDialog
    MOdifications:
        written: Samuel LeBlanc, 2015-09-14, NASA Ames, Santa Cruz, CA
    """
    def __init__(self,pt_list,title='Choose flight',Text='Select points:',parent=None):
        import Tkinter as tk
        if not parent:
            parent = tk._default_root
        self.pt_list = pt_list
        self.Text = Text
        tkSimpleDialog.Dialog.__init__(self,parent,title)
        pass
    
    def body(self,master):
        import tkSimpleDialog
        import Tkinter as tk
        self.results = []
        tk.Label(master, text=self.Text).grid(row=0)
        self.cbuttons = []
        for i,l in enumerate(self.pt_list):
            var = tk.IntVar()
            self.results.append(var)
            self.cbuttons.append(tk.Checkbutton(master,text=l, variable=var))
            self.cbuttons[i].grid(row=i+1,sticky=tk.W)
        return

    def apply(self):
        self.result = map((lambda var: var.get()),self.results)
        return self.result

class Move_point(tkSimpleDialog.Dialog):
    """
    Purpose:
        Dialog box that gets user input for point to add
    Inputs:
        tkSimple.Dialog
        title: title of dialog box (defaults to 'New point info'
    Outputs:
        distance and direction of new point
    Dependencies:
        tkSimpleDialog
    MOdifications:
        written: Samuel LeBlanc, 2015-09-14, NASA Ames, Santa Cruz, CA
    """
    def __init__(self,title='New point info'):
        import Tkinter as tk
        parent = tk._default_root
        tkSimpleDialog.Dialog.__init__(self,parent,title)
        pass
    
    def body(self,master):
        import tkSimpleDialog
        import Tkinter as tk
        tk.Label(master, text='Enter Distance [km]').grid(row=0)
        tk.Label(master, text='Enter Bearing, 0-360, [degrees CW from North]').grid(row=1)
        self.edist = tk.Entry(master)
        self.ebear = tk.Entry(master)
        self.edist.grid(row=0,column=1)
        self.ebear.grid(row=1,column=1)
        return self.edist

    def apply(self):
        self.dist = float(self.edist.get())
        self.bear = float(self.ebear.get())
        return self.dist,self.bear

    def validate(self):
        try:
            self.dist = float(self.edist.get())
            self.bear = float(self.ebear.get())
        except ValueError:
            import tkMessageBox
            tkMessageBox.showwarning('Bad input','Can not format values, try again')
        return True
            
