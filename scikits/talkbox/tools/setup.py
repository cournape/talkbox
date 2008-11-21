from os.path import join
import numpy as np

def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('tools', parent_package, top_path)
    config.add_data_dir('tests')
    config.add_extension('cffilter', ['src/cffilter.c'])
    config.add_extension('cacorr', ['src/cacorr.c'])

    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
