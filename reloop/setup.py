# python f-setup.py build_ext --inplace
#   cython wrapper.pyx -> wrapper.cpp
#   g++ -c wrapper.cpp -> wrapper.o
#   g++ -c fc.cpp -> fc.o
#   link wrapper.o fc.o -> wrapper.so

# distutils uses the Makefile distutils.sysconfig.get_makefile_filename()
# for compiling and linking: a sea of options.

# http://docs.python.org/distutils/introduction.html
# http://docs.python.org/distutils/apiref.html  20 pages ...
# http://stackoverflow.com/questions/tagged/distutils+python

import numpy
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import os
import sys
# from Cython.Build import cythonize

os.environ['CC'] = "g++"

ext_modules = [
    Extension(
    name="reloop.utils.saucywrapper",
    sources=["reloop/utils/saucywrapper.pyx",\
             "reloop/utils/saucy/fc.cpp", \
             "reloop/utils/saucy/saucy.c",\
             "reloop/utils/saucy/main.c",\
             "reloop/utils/saucy/saucyio.c",\
             "reloop/utils/saucy/util.c"],
    include_dirs = [numpy.get_include()],  # .../site-packages/numpy/core/include
    language="c++",
    extra_compile_args = "-ansi -fpermissive -Wall -O0 -ggdb -fPIC".split(),
    extra_link_args = "-lz".split()
        # extra_link_args = "...".split()
    ),
    Extension(
    name="reloop.utils.io.glpkwrap",
    sources=["reloop/utils/io/glpkwrap.pyx",\
             "reloop/utils/io/glpk2py.cpp"],
    include_dirs = [numpy.get_include()],  # .../site-packages/numpy/core/include
    libraries=["glpk"],
    language="c++",
    extra_compile_args = "-ansi -fpermissive -Wall -O0 -ggdb -fPIC".split(),
        # extra_link_args = "...".split()
    )

]

setup(
    name = 'reloop',
    version = "1.2.0",
    packages = ['reloop', 'reloop.solvers', 'reloop.utils', 'reloop.utils.io','reloop.languages','reloop.languages.rlp', 'reloop.languages.rlp.grounding'],
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules,
    )
