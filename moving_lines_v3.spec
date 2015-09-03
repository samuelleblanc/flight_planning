# -*- mode: python -*-
a = Analysis(['moving_lines_v2.py'],
             pathex=['C:\\Users\\sleblan2\\Research\\python_codes\\flight_planning'],
             hiddenimports=['scipy.integrate', 'scipy.integrate.quadpack', 'scipy.integrate._vode', 'scpiy.special._ufuncs'],
             hookspath=['.'],
             runtime_hooks=None)

#a.binaries = a.binaries - [('zmq',None,None),('zmq\\libzmq.pyd',None,None),('zmq.devices.monitoredqueue',None,None),
#			   ('PyQt4',None,None),('qt4_plugins',None,None),('PyQt4.QtSvg',None,None),
#			   ('PyQt4.QtGui',None,None),('PyQt4.QtCore',None,None),
#			   ('_agg',None,None),
#			   ('_wxagg',None,None),
#			   ('_GTKagg',None,None),
#			   ('PySide',None,None),('PySide.QtNetwork',None,None),
#			   ('sqlalchemy.cprocessors',None,None),('sqlalchemy.cresultproxy',None,None),('sqlalchemy.cutils',None,None),
#			   ('pandas',None,None)] 

#for line in open('excludes.txt','r'):
#    a.binaries = a.binaries - [(line.rstrip('\n'),None,None)]

f = open('binaries.txt','w')
for t in a.binaries:
    x,y,z = t
    print x
    f.write(x+'\n')
f.close()

import mpl_toolkits.basemap
import dateutil.zoneinfo
import os 
 
src_basedata = os.path.join(mpl_toolkits.basemap.__path__[0], "data")
tgt_basedata = os.path.join('mpl_toolkits', 'basemap', 'data')

src_dateutil = dateutil.zoneinfo.ZONEINFOFILE
tgt_dateutil = os.path.join('dateutil','zoneinfo')

a.datas = a.datas + [('file.rc','C:\\Users\\sleblan2\\Research\\python_codes\\flight_planning\\file.rc','DATA')]
a.datas = a.datas + Tree(src_basedata, prefix=tgt_basedata)
#a.datas = a.datas + Tree(src_dateutil,prefix=tgt_dateutil)
a.datas = a.datas + [('dateutil/zoneinfo/zoneinfo--latest.tar.gz',dateutil.zoneinfo.ZONEINFOFILE,'DATA')]

pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='moving_lines.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='moving_lines')
