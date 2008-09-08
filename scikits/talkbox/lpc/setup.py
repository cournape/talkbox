from os.path import join

def configuration(parent_package='', top_path=None):
    from numpy.distutils.misc_util import Configuration
    config = Configuration('lpc', parent_package, top_path)

    config.add_library('liblpc', sources=['src/levinson.c'])
    #config.add_extension('_lpc',
    #    sources=['src/levinson.c'],
    #    libraries=libraries,
    #    include_dirs=include_dirs,
    #    **blas_info
    #)

    config.add_data_dir('tests')
    return config

if __name__ == '__main__':
    from numpy.distutils.core import setup
    setup(**configuration(top_path='').todict())
