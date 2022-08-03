from setuptools import setup
from Cython.Build import cythonize
import numpy

setup(name="iterator_cubic_8d", ext_modules=cythonize('iterator_cubic_8d.pyx'),include_dirs=[numpy.get_include()])