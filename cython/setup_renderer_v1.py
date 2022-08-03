from setuptools import setup
from Cython.Build import cythonize

# this file sets up the render module (version 1)

setup(name="renderer_v1", ext_modules=cythonize('renderer_v1.pyx', compiler_directives={'language_level' : "3"}),)