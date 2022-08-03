from setuptools import setup
from Cython.Build import cythonize

setup(name="renderer_v2", ext_modules=cythonize('renderer_v2.pyx'),)