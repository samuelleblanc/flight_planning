# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

def __init__():
    """
       Collection of codes to run some typical map utilities
       
           - spherical_dist: codes to calculate the distance from a certain lat lon points
           - map_ind: find the indices of the closest point 
           - radius_m2deg: return the radius of a circle defined by meters to lat lon degrees, 
           
        details are in the info of each module
    """
    pass

# <codecell>

def spherical_dist(pos1, pos2, r=3958.75):
    "Calculate the distance, in km, from one point to another (can use arrays)"
    import numpy as np
    pos1 = np.array(pos1)
    pos2 = np.array(pos2)
    pos1 = pos1 * np.pi / 180
    pos2 = pos2 * np.pi / 180
    cos_lat1 = np.cos(pos1[..., 0])
    cos_lat2 = np.cos(pos2[..., 0])
    cos_lat_d = np.cos(pos1[..., 0] - pos2[..., 0])
    cos_lon_d = np.cos(pos1[..., 1] - pos2[..., 1])
    return r * np.arccos(cos_lat_d - cos_lat1 * cos_lat2 * (1 - cos_lon_d))

# <codecell>

def bearing(pos1,pos2):
    "Calculate the initial bearing, in degrees, to go from one point to another, along a great circle"
    import numpy as np
    pos1 = np.array(pos1)
    pos2 = np.array(pos2)
    pos1 = pos1 * np.pi / 180
    pos2 = pos2 * np.pi / 180
    cos_lat1 = np.cos(pos1[..., 0])
    cos_lat2 = np.cos(pos2[..., 0])
    sin_lat1 = np.sin(pos1[...,0])
    sin_lat2 = np.sin(pos2[...,0])
    sin_lon_d = np.sin(pos1[...,1]-pos2[...,1])
    cos_lat_d = np.cos(pos1[..., 0] - pos2[..., 0])
    cos_lon_d = np.cos(pos1[..., 1] - pos2[..., 1])
    return (np.arctan2(sin_lon_d*cos_lat2,cos_lat1*sin_lat2-sin_lat1*cos_lat2*cos_lon_d)*180.0/np.pi+360.0) % 360.0

# <codecell>

def map_ind(mod_lon,mod_lat,meas_lon,meas_lat,meas_good=None):
    """ Run to get indices in the measurement space of all the closest mod points. Assuming earth geometry."""
    from map_utils import spherical_dist
    from Sp_parameters import startprogress, progress, endprogress
    import numpy as np
    try:
        if not meas_good:
            meas_good = np.where(meas_lon)
    except ValueError:
        if not meas_good.any():
            meas_good = np.where(meas_lon)
        
    imodis = np.logical_and(np.logical_and(mod_lon>min(meas_lon[meas_good])-0.02 , mod_lon<max(meas_lon[meas_good])+0.02),
                            np.logical_and(mod_lat>min(meas_lat[meas_good])-0.02 , mod_lat<max(meas_lat[meas_good])+0.02))
    wimodis = np.where(imodis)
    if not wimodis[0].any():
        print '** No points found within range +/- 0.02 in lat and lon, Extending range to +/- 0.2 **'
        imodis = np.logical_and(np.logical_and(mod_lon>min(meas_lon[meas_good])-0.2 , mod_lon<max(meas_lon[meas_good])+0.2),
                                np.logical_and(mod_lat>min(meas_lat[meas_good])-0.2 , mod_lat<max(meas_lat[meas_good])+0.2))
        wimodis = np.where(imodis)
        if not wimodis[0].any():
            print '** No points found in extended range, returning null **'
            return []
    N1 = mod_lon[imodis].size
    modis_grid = np.hstack([mod_lon[imodis].reshape((N1,1)),mod_lat[imodis].reshape((N1,1))])
    try:
        N2 = len(meas_good)
        if N2==1 or N2==2:
            meas_good = meas_good[0]
            N2 = len(meas_good)
        meas_grid = np.hstack([np.array(meas_lon[meas_good]).reshape((N2,1)),np.array(meas_lat[meas_good]).reshape((N2,1))])
    except:
        import pdb; pdb.set_trace()
    meas_in = meas_grid.astype(int)
    meas_ind = np.array([meas_good.ravel()*0,meas_good.ravel()*0])
    startprogress('Running through flight track')
    for i in xrange(meas_good.size):
        d = spherical_dist(meas_grid[i],modis_grid)
        try:
            meas_ind[0,i] = wimodis[0][np.argmin(d)]
        except:
            import pdb; pdb.set_trace()
        meas_ind[1,i] = wimodis[1][np.argmin(d)]
        progress(float(i)/len(meas_good)*100)
    endprogress()
    return meas_ind

# <codecell>

def radius_m2deg(center_lon,center_lat,radius):
    """ 
    Return the radius in lat lon degrees of a circle centered at the points defined by
      center_lon
      center_lat
    with a radius defined in meters by:
      radius
      
    Dependencies:
        
        - geopy library
    """
    import geopy
    from geopy.distance import VincentyDistance
    origin = geopy.Point(center_lat,center_lon)
    destination = VincentyDistance(kilometers=radius/1000.0).destination(origin,0.0)
    radius_degrees = abs(center_lat-destination.latitude)
    return radius_degrees

# <codecell>

def stats_within_radius(lat1,lon1,lat2,lon2,x2,radius,subset=True):
    """
    Run through all points defined by lat1 and lon1 (can be arrays)
    to find the points within defined by lat2 and lon2 that are within a distance in meters defined by radius
    lat2, lon2, x2 can be multidimensional, will be flattened first
    if subset (optional) is set to True, and there are more than 100 points, only every 10th in lat1, lon1 will be used.
    Returns a dicttionary of statistics:
        'index' : array of indices of flattened lat2 and lon2 that are within radius meters of each point of lat1 and lon1
        'std' : array of standard deviation of x2 that are near lat1 and lon1 by radius
        'range' : range of values of x2 near lat1, lon1
        'mean' : mean of values of x2 near lat1, lon1
        'median': median values of x2 near lat1, lon1
    """
    from scipy.spatial import cKDTree
    from map_utils import radius_m2deg
    import numpy as np
    print 'Setting up the lat, lon, localization'
    max_distance = radius_m2deg(lon1[0],lat1[0],radius) #transform to degrees
    if (len(lat1) > 100) & subset:
        points_ref = np.column_stack((lat1[::10],lon1[::10]))
    else:
        points_ref = np.column_stack((lat1,lon1))
    if len(lat2.shape) > 1:
        points = np.column_stack((lat2.reshape(lat2.size),lon2.reshape(lon2.size)))
        xx = x2.reshape(x2.size)
    else:
        points = np.column_stack((lat2,lon2)) 
        xx = x2
    tree = cKDTree(points)
    tree_ref = cKDTree(points_ref)
    out = dict()
    print '... Getting the index points'
    out['index'] = tree_ref.query_ball_tree(tree,max_distance)
    out['std'] = []
    out['range'] = []
    out['mean'] = []
    out['median'] = []
    print '... Running through index points'
    for i in out['index']:
        if not i:
            out['std'].append(np.NaN)
            out['range'].append(np.NaN)
            out['mean'].append(np.NaN)
            out['median'].append(np.NaN)
        else:
            out['std'].append(np.nanstd(xx[i]))
            out['range'].append(np.nanmax(xx[i])-np.nanmin(xx[i]))
            out['mean'].append(np.nanmean(xx[i]))
            out['median'].append(np.median(xx[i]))
    out['std'] = np.array(out['std'])
    out['range'] = np.array(out['range'])
    out['mean'] = np.array(out['mean'])
    out['median'] = np.array(out['median'])
    print out.keys()
    return out

