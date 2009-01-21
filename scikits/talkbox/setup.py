import os
from os.path import join

def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration, get_numpy_include_dirs
    config = Configuration('talkbox', parent_package, top_path)
    config.add_subpackage('features')
    config.add_subpackage('linpred')
    config.add_subpackage('spectral')
    config.add_subpackage('transforms')
    config.add_subpackage('tools')
    config.add_subpackage('misc')
    return config

if __name__ == "__main__":
    from numpy.distutils.core import setup
    config = configuration(top_path='').todict()
    setup(**config)
