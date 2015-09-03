from mpl_toolkits.basemap import Basemap
import numpy as np
import sys
import re
import copy

import map_interactive as mi
from map_utils import spherical_dist,equi,shoot

class LineBuilder:
    """
    Purpose:
        create interaction via plotting lines and clickable map
    Inputs: (at init)
        line from a single plot
        m: basemap base class
        ex: excel_interface class
        verbose: (default False) writes out comments along the way
        tb: toolbar instance to use its interactions.
    Outputs:
        LineBuilder class 
    Dependencies:
        numpy
        map_utils
        sys
        Basemap
    Required files:
        none
    Example:
        ...
    Modification History:
        Written: Samuel LeBlanc, 2015-08-07, Santa Cruz, CA
        Modified: Samuel LeBlanc, 2015-08-21, Santa Cruz, CA
                 - added new plotting with range circles
    """
    def __init__(self, line,m=None,ex=None,verbose=False,tb=None):
        """
        Start the line builder, with line2d object as input,
        and opitonally the m from basemap object,
        Optionally the ex, dict_position class from the excel_interface,
            for interfacing with Excel spreadsheet
        
        """
	self.line = line
        self.line_arr = []
        self.line_arr.append(line)
        self.iactive = 0
        self.m = m
        self.ex = ex
        self.ex_arr = []
        self.ex_arr.append(ex)
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        if self.m:
            self.lons,self.lats = self.m(self.xs,self.ys,inverse=True)
        self.connect()
        self.line.axes.format_coord = self.format_position_simple
        self.press = None
        self.contains = False
        self.labelsoff = False
        self.circlesoff = False
        self.lbl = None
        self.verbose = verbose
        if not tb:
         #   import matplotlib.pyplot as plt
         #   self.tb = plt.get_current_fig_manager().toolbar
            print 'No tb set, will not work'
        else:
            self.tb = tb

    def connect(self):
        'Function to connect all events'
        self.cid_onpress = self.line.figure.canvas.mpl_connect(
            'button_press_event', self.onpress)
        self.cid_onrelease = self.line.figure.canvas.mpl_connect(
            'button_release_event', self.onrelease)
        self.cid_onmotion = self.line.figure.canvas.mpl_connect(
            'motion_notify_event',self.onmotion)
        self.cid_onkeypress = self.line.figure.canvas.mpl_connect(
            'key_press_event',self.onkeypress)
        self.cid_onkeyrelease = self.line.figure.canvas.mpl_connect(
            'key_release_event',self.onkeyrelease)
        self.cid_onfigureenter = self.line.figure.canvas.mpl_connect(
            'figure_enter_event',self.onfigureenter)
        self.cid_onaxesenter = self.line.figure.canvas.mpl_connect(
            'axes_enter_event',self.onfigureenter)

    def disconnect(self):
        'Function to disconnect all events (except keypress)'
        self.line.figure.canvas.mpl_disconnect(self.cid_onpress)
        self.line.figure.canvas.mpl_disconnect(self.cid_onrelease)
        self.line.figure.canvas.mpl_disconnect(self.cid_onmotion)
        self.line.figure.canvas.mpl_disconnect(self.cid_onkeyrelease)

    def onpress(self,event):
        'Function that enables either selecting a point, or creating a new point when clicked'
        #print 'click', event
        if event.inaxes!=self.line.axes: return
        if self.tb.mode!='': return
        self.contains, attrd = self.line.contains(event)
        if self.contains:
            if self.verbose:
                print 'click is near point:',self.contains,attrd
            self.contains_index = attrd['ind']
            if len(self.contains_index)>1:
                self.contains_index = self.contains_index[-1]
            if self.verbose:
                print 'index:%i'%self.contains_index
            if self.contains_index != 0:
                self.xy = self.xs[self.contains_index-1],self.ys[self.contains_index-1]
                self.line.axes.format_coord = self.format_position_distance
                self.line.axes.autoscale(enable=False)
                self.highlight_linepoint, = self.line.axes.plot(self.xs[self.contains_index],
                                                            self.ys[self.contains_index],'bo')
            else:
                self.line.axes.format_coord = self.format_position_simple
                self.xy = self.xs[-1],self.ys[-1]
                self.xs.append(self.xs[self.contains_index])
                self.ys.append(self.ys[self.contains_index])
                if self.m:
                    lo,la = self.m(self.xs[self.contains_index],self.ys[self.contains_index],inverse=True)
                    self.lons.append(lo)
                    self.lats.append(la)
                self.contains = False
            ilola = self.contains_index
        else:
            self.xy = self.xs[-1],self.ys[-1]
            self.xs.append(event.xdata)
            self.ys.append(event.ydata)
            if self.m:
                lo,la = self.m(event.xdata,event.ydata,inverse=True)
                self.lons.append(lo)
                self.lats.append(la)
            self.line.axes.format_coord = self.format_position_distance
            ilola = -2
        self.line.set_data(self.xs, self.ys)
        self.line.range_circles,self.line.range_cir_anno = self.plt_range_circles(self.lons[ilola],self.lats[ilola])
        self.line.figure.canvas.draw()
        self.press = event.xdata,event.ydata
        if self.verbose:
            sys.stdout.write('moving:')
            sys.stdout.flush()
        
    def onrelease(self,event):
        'Function to set the point location'
        
        if self.verbose:
            print 'release'#,event

        if (self.tb.mode == 'zoom rect') | (self.tb.mode == 'pan/zoom') | (self.tb.mode!=''):
            ylim = self.line.axes.get_ylim()
            xlim = self.line.axes.get_xlim()
            self.m.llcrnrlon = xlim[0]
            self.m.llcrnrlat = ylim[0]
            self.m.urcrnrlon = xlim[1]
            self.m.urcrnrlat = ylim[1]
            if (xlim[1]-xlim[0])<20.0:
                mer = np.linspace(-14,20,18).astype(int)
            else:
                mer = np.linspace(-15,20,8).astype(int)
            if (ylim[1]-ylim[0])<20.0:
                par = np.linspace(-24,4,15).astype(int)
            else:
                par = np.linspace(-25,5,7).astype(int)
            mi.update_pars_mers(self.m,mer,par)
### Need to update
            self.line.figure.canvas.draw()
            return
        elif self.tb.mode!='':
            return
        
        if event.inaxes!=self.line.axes: return
        self.press = None
        self.line.axes.format_coord = self.format_position_simple
        
        if self.contains:
            hlight = self.highlight_linepoint.findobj()[0]
            while hlight in self.line.axes.lines:
                self.line.axes.lines.remove(hlight)
            self.contains = False
            if self.ex:
                self.ex.mods(self.contains_index,
                             self.lats[self.contains_index],
                             self.lons[self.contains_index])
                self.ex.calculate()
                self.ex.write_to_excel()
        else:
            if self.ex:
                self.ex.appends(self.lats[-1],self.lons[-1])
                self.ex.calculate()
                self.ex.write_to_excel()
        for lrc in self.line.range_circles:
            self.m.ax.lines.remove(lrc)
        for arc in self.line.range_cir_anno:
            try:
                arc.remove()
            except:
                continue
        self.update_labels()
        self.line.figure.canvas.draw()
            

    def onmotion(self,event):
        'Function that moves the points to desired location'
        if event.inaxes!=self.line.axes: return
        if self.press is None: return
        if self.tb.mode!='': return
        if self.verbose:
            sys.stdout.write("\r"+" moving: x=%2.5f, y=%2.5f" %(event.xdata,event.ydata))
            sys.stdout.flush()
        if self.contains:
            i = self.contains_index
            self.highlight_linepoint.set_data(event.xdata,event.ydata)
        else:
            i = -1
        self.xs[i] = event.xdata
        self.ys[i] = event.ydata
        if self.m:
            self.lons[i],self.lats[i] = self.m(event.xdata,event.ydata,inverse=True)
        self.line.set_data(list(self.xs),list(self.ys))
        self.line.figure.canvas.draw()

    def onkeypress(self,event):
        'function to handle keyboard events'
        if self.verbose:
            print 'pressed key',event.key,event.xdata,event.ydata
        if event.inaxes!=self.line.axes: return
        if (event.key=='s') | (event.key=='alt+s'):
            print 'Stopping interactive point selection'
            self.disconnect()
        if (event.key=='i') | (event.key=='alt+i'):
            print 'Starting interactive point selection'
            self.connect()
            self.line.axes.format_coord = self.format_position_simple
            self.press = None
            self.contains = False

    def onkeyrelease(self,event):
        'function to handle keyboard releases'
        #print 'released key',event.key
        if event.inaxes!=self.line.axes: return

    def onfigureenter(self,event):
        'event handler for updating the figure with excel data'
        self.line.axes.format_coord = 'Calculating ...'
        if self.verbose:
            print 'entered figure'#, event
        if self.ex:
            #self.ex.switchsheet(self.iactive)
            self.ex.check_xl()
            self.lats = list(self.ex.lat)
            self.lons = list(self.ex.lon)
            if self.m:
                x,y = self.m(self.ex.lon,self.ex.lat)
                self.xs = list(x)
                self.ys = list(y)
                self.line.set_data(self.xs,self.ys)
                self.line.figure.canvas.draw()
        self.update_labels()
        self.line.axes.format_coord = 'Done Calculating!'
        self.line.axes.format_coord = self.format_position_simple
                
    def format_position_simple(self,x,y):
        'format the position indicator with only position'
        if self.m:
            return 'Lon=%.7f, Lat=%.7f'%(self.m(x, y, inverse = True))
        else:   
            return 'x=%2.5f, y=%2.5f' % (x,y)

    def format_position_distance(self,x,y):
        'format the position indicator with distance from previous point'
        if self.m:
            x0,y0 = self.xy
            lon0,lat0 = self.m(x0,y0,inverse=True)
            lon,lat = self.m(x,y,inverse=True)
            r = spherical_dist([lat0,lon0],[lat,lon])
            return 'Lon=%.7f, Lat=%.7f, d=%.2f km'%(lon,lat,r)
        else:
            x0,y0 = self.xy
            self.r = sqrt((x-x0)**2+(y-y0)**2)
            return 'x=%2.5f, y=%2.5f, d=%2.5f' % (x,y,self.r)
        
    def update_labels(self):
        'method to update the waypoints labels after each recalculations'
        #import matplotlib as mpl
        #if mpl.rcParams['text.usetex']:
        #    s = '\#'
        #else:
        #    s = '#'
        s = '#'
        if self.ex:
            self.wp = self.ex.WP
        else:
            self.n = len(self.xs)
            self.wp = range(1,self.n+1)
        if self.lbl:
           for ll in self.lbl:
                try:
                    ll.remove()
                except:
                    continue
        if self.labelsoff:
            return
        for i in self.wp:    
            if not self.lbl:
                self.lbl = [self.line.axes.annotate(s+'%i'%i,
                                                    (self.xs[i-1],self.ys[i-1]))]
            else:
                self.lbl.append(self.line.axes.
                                annotate(s+'%i'%i,(self.xs[i-1],self.ys[i-1])))
        self.line.figure.canvas.draw()

    def plt_range_circles(self,lon,lat):
        'program to plot range circles starting from the last point selected on the map'        
        if self.circlesoff:
            return
        diam = [50.0,100.0,200.0,500.0,1000.0]
        colors = ['lightgrey','lightgrey','lightgrey','lightsalmon','crimson']
        line = []
        an = []
        for i,d in enumerate(diam):
            ll, = equi(self.m,lon,lat,d,color=colors[i])
            line.append(ll)
            slon,slat,az = shoot(lon,lat,0.0,d)
            x,y = self.m(slon,slat)
            ano = self.line.axes.annotate('%i km' %(d),(x,y),color='silver')
            an.append(ano)
        return line,an

    def makegrey(self):
        'Program to grey out the entire path'
        self.line.set_color('#AAAAAA')
        ### need to debug here
        
    def colorme(self,c):
        'Program to color the entire path'
        self.line.set_color(c)

    def newline(self):
        'Program to do a deep copy of the line object in the LineBuilder class'
        self.line_arr.append(copy.copy(self.line))

def build_basemap(lower_left=[-20,-30],upper_right=[20,10],ax=None,proj='cyl'):
    """
    First try at a building of the basemap with a 'stere' projection
    Must put in the values of the lower left corner and upper right corner (lon and lat)
    
    Defaults to draw 8 meridians and parallels
    """
    m = Basemap(projection=proj,lon_0=(upper_right[0]+lower_left[0]),lat_0=(upper_right[1]+lower_left[1]),
            llcrnrlon=lower_left[0], llcrnrlat=lower_left[1],
            urcrnrlon=upper_right[0], urcrnrlat=upper_right[1],resolution='h',ax=ax)
    m.artists = []
    m.drawcoastlines()
    #m.fillcontinents(color='#AAAAAA')
    m.drawstates()
    m.drawcountries()
    mer = np.linspace(-15,20,8).astype(int)
    #mer = np.linspace(lower_left[0],upper_right[0],8).astype(int)
    par = np.linspace(-25,5,7).astype(int)
    #par = np.linspace(lower_left[1],upper_right[1],8).astype(int)
    m.artists.append(m.drawmeridians(mer,labels=[0,0,0,1]))
    m.artists.append(m.drawparallels(par,labels=[1,0,0,0]))
    return m

def update_pars_mers(m,meridians,parallels):
    'Simple program to remove old meridians and parallels and plot new ones'
    r = 0
    for a in m.artists:
        try:
            a.remove()
        except AttributeError:
            for b in a.values():
                try:
                    b.remove()
                except:
                    for c in b:
                        try:
                            c.remove()
                        except:
                            for d in c:
                                try:
                                    d.remove()
                                except:
                                    r = r+1

    m.artists = []
    m.artists.append(m.drawmeridians(meridians,labels=[0,0,0,1]))
    m.artists.append(m.drawparallels(parallels,labels=[1,0,0,0]))

def pll(string):
    """
    pll for parse_lat_lon
    function that parses a string and converts it to lat lon values
    one space indicates seperation between degree, minutes, or minutes and seconds
    returns decimal degrees
    """
    if type(string) is float:
        return string
    n = len(string.split())
    str_ls = string.split()
    char_neg = re.findall("[SWsw]+",str_ls[-1])
    char_pos = re.findall("[NEne]+",str_ls[-1])
    if len(char_neg)>0:
        sign = -1
        cr = char_neg[0]
    elif len(char_pos)>0:
        sign = 1
        cr = char_pos[0]
    else:
        sign = 1
        cr = ''
    str_ls[-1] = str_ls[-1].strip(cr)
    deg = float(str_ls[0])*sign
    deg_m = 0.0
    for i in range(n-1,0,-1):
        deg_m = deg_m/60.0
        deg_m = deg_m + float(str_ls[i])/60.0
    return deg+(deg_m*sign)

def plot_map_labels(m,filename,marker=None,skip_lines=0,color='k'):
    """
    program to plot the map labels on the basemap plot defined by m
    if marker is set, then it will be the default for all points in file
    """
    labels = mi.load_map_labels(filename,skip_lines=skip_lines) 
    for l in labels:
        try:
            x,y = m(l['lon'],l['lat'])
            xtxt,ytxt = m(l['lon']+0.05,l['lat'])
        except:
            x,y = l['lon'],l['lat']
            xtxt,ytxt = l['lon']+0.05,l['lat']
        if marker:
            ma = marker
        else:
            ma = l['marker'] 
        m.plot(x,y,color=color,marker=ma)
        m.ax.annotate(l['label'],(xtxt,ytxt))

def load_map_labels(filename,skip_lines=0):
    """
    Program to load map labels from a text file, csv
    with format: Label, lon, lat, style
    returns list of dictionary with each key as the label
    """
    out = []
    with open(filename,'r') as f:
        for i in range(skip_lines):
            next(f)
        for line in f:
            sp = line.split(',')
            if sp[0].startswith('#'):
                continue
            out.append({'label':sp[0],'lon':mi.pll(sp[1]),'lat':mi.pll(sp[2]),'marker':sp[3].rstrip('\n')})
    return out

def load_sat_from_net():
    """
    Program to load the satllite track prediction from the internet
    Checks at the avdc website
    """
    import time
    from urllib2 import urlopen
    from pykml import parser
    today = time.strftime('%Y%m%d')
    site = 'http://avdc.gsfc.nasa.gov/download_2.php?site=98675770&id=25&go=download&path=%2FSubsatellite%2Fkml&file=A-Train_subsatellite_prediction_'+today+'T000000Z.kml'
    response = urlopen(site)
    print 'Getting the kml prediction file from avdc.gsfc.nasa.gov'
    r = response.read()
    kml = parser.fromstring(r)
    print 'Kml file read...'
    return kml

def load_sat_from_file(filename):
    """
    Program to load the satellite track prediction from a saved file
    """
    from pykml import parser
    f = open(filename,'r')
    r = f.read()
    kml = parser.fromstring(r)
    return kml

def get_sat_tracks(datestr,kml):
    """
    Program that goes and fetches the satellite tracks for the day
    For the day defined with datestr
    kml is the parsed kml structure with pykml
    """
    from map_interactive import pll
    sat = dict()
    # properly format datestr
    day = datestr.replace('-','')
    for i in range(4):
        name = str(kml.Document.Document[i].name).split(':')[1].lstrip(' ')
        for j in range(1,kml.Document.Document[i].countchildren()-1):
            if str(kml.Document.Document[i].Placemark[j].name).find(day) > 0:
                pos_str = str(kml.Document.Document[i].Placemark[j].LineString.coordinates)
                post_fl = pos_str.split(' ')
                lon,lat = [],[]
                for s in post_fl:
                    try:
                        x,y = s.split(',')
                        lon.append(pll(x))
                        lat.append(pll(y))
                    except:
                        pass
        try:
            sat[name] = (lon,lat)
        except UnboundLocalError:
            print 'Skipping %s; no points downloaded' %name
    return sat

def plot_sat_tracks(m,sat):
    """
    Program that goes through and plots the satellite tracks
    """
    for k in sat.keys():
        (lon,lat) = sat[k]
        x,y = m(lon,lat)
        m.plot(x,y,'.',label=k)
    m.ax.legend(loc='lower right',bbox_to_anchor=(1.0,1.04))

        
    
