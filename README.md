# ikfast_pybind - generating unified python bindings for IKFast
<!-- [![Build Status](https://travis-ci.com/yijiangh/conmech.svg?branch=master)](https://travis-ci.com/yijiangh/conmech) -->

[![GitHub - License](https://img.shields.io/github/license/yijiangh/conmech)](./LICENSE)

<!-- [![PyPI - Python Version](https://img.shields.io/badge/python-2.5+|3.x-blue)](https://pypi.org/project/pyconmech/)

[![PyPI - Latest Release](https://img.shields.io/badge/pypi-v0.1.1-orange)](https://pypi.org/project/pyconmech/) -->

**ikfast_pybind** is a python binding generation library for the analytic kinematics engine [IKfast](http://openrave.org/docs/1.8.2/openravepy/ikfast/). The python bindings are generated via [pybind11](https://github.com/pybind/pybind11) a [CMake](https://cmake.org/)-based build system.

**Note:** You need the ikfast `.h` and `.cpp` ready to generate the python bindings. This *URDF-to-cpp* generation part needs to be done with `openrave` and **IS NOT** done by this repo, please see [this tutorial](https://github.com/yijiangh/Choreo/blob/7c98fd29120e5ce75d2b8ed17bc49488ad983cb6/framefab_robot/abb/framefab_irb6600/framefab_irb6600_support/doc/ikfast_tutorial.rst) for details.

The assembly sequence and motion planning framework [pychoreo](https://github.com/yijiangh/pychoreo) relies on this library to generate compatible IK modules for robots across brands, scales, and dofs.

## Prerequisites

*ikfast_pybind* depends on the following dependencies, which come from [pybind11] for building the python bindings.

**On Unix (Linux, OS X)**

* A compiler with C++11 support
* CMake >= 2.8.12

**On Windows**

* Visual Studio 2015 (required for all Python versions, see notes below)
* CMake >= 3.1

**It is recommended (especially for Windows users) to test the environment with the [cmake_example for pybind11](https://github.com/pybind/cmake_example) before proceeding to build conmech.**

## Installation

```bash
git clone --recursive https://github.com/yijiangh/ikfast_pybind
cd ikfast_pybind
pip install .
# try with '--user' if you encountered a sudo problem
```
For developers:

```bash
git clone --recursive https://github.com/yijiangh/ikfast_pybind
cd ikfast_pybind
python setup.py sdist
pip install --verbose dist/*.tar.gz
```

With the `setup.py` file included in the base folder, the pip install command will invoke CMake and build the pybind11 module as specified in CMakeLists.txt.

<!-- ```
pip install ikfast_pybind
``` -->

## References

### Citation

If you find [IKFast](http://openrave.org/docs/0.8.2/openravepy/ikfast/) useful, please cite [OpenRave](http://openrave.org/):

```
@phdthesis{diankov_thesis,
  author = "Rosen Diankov",
  title = "Automated Construction of Robotic Manipulation Programs",
  school = "Carnegie Mellon University, Robotics Institute",
  month = "August",
  year = "2010",
  number= "CMU-RI-TR-10-29",
  url={http://www.programmingvision.com/rosen_diankov_thesis.pdf},
}
```

### Related links

[tutorial on ikfast cpp generation](https://github.com/yijiangh/Choreo/blob/7c98fd29120e5ce75d2b8ed17bc49488ad983cb6/framefab_robot/abb/framefab_irb6600/framefab_irb6600_support/doc/ikfast_tutorial.rst): See this tutorial for a detailed instruction on how to generate the ikfast cpp code from an URDF.

[Testing ikfast modules with a pick-n-place demo in pybullet](https://github.com/yijiangh/conrob_pybullet/tree/master/debug_examples)

[ur_kinematics](http://wiki.ros.org/ur_kinematics): Provides forward and inverse kinematics for Universal Robots. This repo is a part of [ROS Industrial](http://wiki.ros.org/Industrial) program.

[ikfastpy](https://github.com/andyzeng/ikfastpy): Python wrapper over OpenRave's IKFast inverse kinematics solver for a UR5 robot arm.

[pybind11]: https://github.com/pybind/pybind11
