# -*- mode: python -*-
a = Analysis(['moving_lines_v2.py'],
             pathex=['C:\\Users\\sleblan2\\Research\\python_codes\\flight_planning'],
             hiddenimports=[],
             hookspath=['.'],
             runtime_hooks=None)
pyz = PYZ(a.pure)


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
a.datas = a.datas + [('aeronet_locations.txt','C:\\Users\\sleblan2\\Research\\python_codes\\flight_planning\\aeronet_locations.txt','DATA')]
a.datas = a.datas  + [('labels.txt','C:\\Users\\sleblan2\\Research\\python_codes\\flight_planning\\labels.txt','DATA')]

exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='moving_lines_v2.exe',
          debug=True,
          strip=None,
          upx=True,
          console=True )

coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='moving_lines_v2')
