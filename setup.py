import os
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
    # 'cmake>=3.18',
]

# scan for all ikfast modules in the src folder
src_path = os.path.join(ROOT_DIR, 'src')
module_names = [f.name for f in os.scandir(src_path) if f.is_dir() and not f.name.startswith('_')]
print('Building ikfast modules: {}'.format(module_names))
ext_modules = [CMakeExtension(m_name) for m_name in module_names]

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