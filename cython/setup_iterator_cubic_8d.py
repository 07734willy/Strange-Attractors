from setuptools import setup
from Cython.Build import cythonize
import numpy

# this file sets up the cython iteration module

setup(name="iterator_cubic_8d", ext_modules=cythonize('iterator_cubic_8d.pyx'),include_dirs=[numpy.get_include()])