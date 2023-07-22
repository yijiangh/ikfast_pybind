import os, sys
import argparse
import io

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext
from distutils.version import LooseVersion
from setup_cmake_utils import CMakeExtension, CMakeBuild
from setuptools.command.install import install


ROOT_DIR = os.path.abspath(os.path.dirname(__file__))


def read(*names, **kwargs):
    return io.open(
        os.path.join(ROOT_DIR, *names),
        encoding=kwargs.get('encoding', 'utf8')
    ).read()


long_description = read('README.md')

requirements = [
    'numpy>=1.21.5, <2.0.0',
]

# modified from https://github.com/primme/primme/blob/master/Python/setup.py
# https://github.com/primme/primme/issues/37#issuecomment-692066436
def get_numpy_options():
   # Third-party modules - we depend on numpy for everything
   import numpy
   try:
       from numpy.distutils.system_info import get_info
   except:
       from numpy.__config__ import get_info
   
   # Obtain the numpy include directory
   numpy_include = numpy.get_include()

   # Obtain BLAS/LAPACK linking options
   lapack_info = get_info('lapack_opt')
   blas_info = get_info('blas_opt')
   using_atlas = False
   using_f77blas = False
   using_lapack = False
   for l in lapack_info.get('libraries', []) + blas_info.get('libraries', []):
      if "atlas" in l: using_atlas = True
      if "f77blas" in l: using_f77blas = True
      if "lapack" in l: using_lapack = True
   if using_atlas and (not using_f77blas or not using_lapack):
      lapack_info = get_info('atlas')
      # ATLAS notices an incomplete LAPACK by not setting language to f77
      complete_lapack = lapack_info.get('language', "") == "f77"
      if complete_lapack:
         blas_info = {}
      else:
         # If ATLAS has an incomplete LAPACK, use a regular one
         blas_info = get_info('atlas_blas')
         lapack_info = get_info('lapack')
   
   blaslapack_libraries = lapack_info.get('libraries', []) + blas_info.get('libraries', [])
   blaslapack_library_dirs = lapack_info.get('library_dirs', []) + blas_info.get('library_dirs', [])
   blaslapack_extra_link_args = lapack_info.get('extra_link_args', []) + blas_info.get('extra_link_args', [])
   if not blaslapack_libraries and not blaslapack_extra_link_args:
       blaslapack_libraries = ['lapack', 'blas']

   r = dict(
                   include_dirs = [numpy_include, "primme/include", "primme/src/include"],
                   library_dirs = blaslapack_library_dirs,
                   libraries = blaslapack_libraries,
                   extra_link_args = blaslapack_extra_link_args
   )

   return r

try:
   import numpy
except:
   raise Exception("numpy not installed; please, install numpy before primme")
else:
   extra_options = get_numpy_options()

# scan for all ikfast modules in the src folder
src_path = os.path.join(ROOT_DIR, 'src')
module_names = [f.name for f in os.scandir(src_path) if f.is_dir() and not (f.name.startswith('_') or f.name.endswith('.egg-info'))]
print('Building ikfast modules: {}'.format(module_names))
ext_modules = [CMakeExtension(m_name) for m_name in module_names]
for m in ext_modules:
   m.set_lapack_libs(extra_options['library_dirs'], extra_options['libraries'])
   print(m.lapack_lib_paths)

setup(
    name='ikfast_pybind',
    version='0.1.1',
    license='MIT License',
    description='ikfast_pybind is a python binding generation library for the analytic kinematics engine ikfast.',
    author='Yijiang Huang',
    author_email='yijiangh@mit.edu',
    url="https://github.com/yijiangh/ikfast_pybind",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # packages=['ikfast_pybind'],
    # package_dir={'': 'src'},
    ext_modules=ext_modules,
    cmdclass=dict(build_ext=CMakeBuild),
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        "License :: OSI Approved :: MIT License",
        'Operating System :: Unix',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords=['Robotics', 'kinematics'],
    install_requires=requirements,
)