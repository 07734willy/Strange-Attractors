from setuptools import setup
from Cython.Build import cythonize

setup(name="renderer_v1", ext_modules=cythonize('renderer_v1.pyx', compiler_directives={'language_level' : "3"}),)