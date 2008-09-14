import os
from os.path import join

def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration, get_numpy_include_dirs
    confgr = Configuration('', parent_package, top_path)
    confgr.add_subpackage('lpc')
    return confgr

if __name__ == "__main__":
    from numpy.distutils.core import setup
    config = configuration(top_path='').todict()
    setup(**config)
