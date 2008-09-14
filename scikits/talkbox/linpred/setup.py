from os.path import join
import numpy as np

def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('linpred', parent_package, top_path)

    config.add_library('clpc', sources=['src/levinson.c'])

    config.add_extension('_lpc', sources=["src/_lpc.c"],
                         include_dirs=[np.get_include()],
                         libraries=["clpc"])
    config.add_data_dir('tests')

    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
