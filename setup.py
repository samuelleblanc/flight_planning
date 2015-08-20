from distutils.core import setup
import zmq.libzmq
import matplotlib
import py2exe,sys,os

sys.argv.append('py2exe')

py2exeopts = {'bundle_files':1,
              'compressed':True,
              'includes':['zmq.backend.cython',
                          'matplotlib'],
              'excludes':['zmq.libzmq',
                          '_gtkagg','_wxagg','_agg2', 
                          '_cairo', '_cocoaagg',
                          '_fltkagg', '_gtk', '_gtkcairo'],
              'dll_excludes':['libzmq.pyd',
                              'libgdk-win32-2.0-0.dll',
                              'libgobject-2.0-0.dll'],
              'packages':['matplotlib']
              }

setup(
    windows = [{'script':'moving_lines.py'}],
    options = {'py2exe':py2exeopts},
    zipfile = None,
    data_files = [('text',['file.rc']),
                  ('lib',[zmq.libzmq.__file__,matplotlib.get_py2exe_datafiles()])]
    )
