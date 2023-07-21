
# ikfast_pybind

[![Github Actions Build Status](https://github.com/yijiangh/ikfast_pybind/workflows/build/badge.svg)](https://github.com/compas-dev/compas_fab/actions)
[![License](https://img.shields.io/github/license/yijiangh/ikfast_pybind.svg)](https://pypi.python.org/pypi/ikfast_pybind)

**ikfast_pybind** is a python binding generation library for the analytic kinematics engine [IKfast](http://openrave.org/docs/1.8.2/openravepy/ikfast/). 
The python bindings are generated via [pybind11](https://github.com/pybind/pybind11) a [CMake](https://cmake.org/)-based build system.

## Main features

Analytical inverse and forward kinematics (IK and FK) for robots with **less or equal than six degrees of freedom**. 
For a given end effector pose, ikfast computes **all** IK solutions (e.g. 8 solutions for a 6-dof robot).
The ikfast backend is C++ code, and it only performs geometric kinematic computations, it is fast and deterministic.

However, **ikfast knows nothing about the robot's joint limits and collision models**, so it is up to the user to filter the solutions and check for collisions.

**Note:** 
`ikfast_pybind` contains a few commonly used industrial robot models to allow pip install and quick use.
`ikfast_pybind` includes the ikfast cpp code for these robots, but it mainly takes care of the compilation and wrapping of the ikfast cpp code into python bindings.

THe actual ikfast cpp code generation from a given robot model is done by OpenRave's ikfast module, which is not included in this library.
If you want to add new robot models from URDF files, please refer to the [Adding new robots](#adding-new-robots) section.

## Installation

```
  git clone --recursive https://github.com/yijiangh/ikfast_pybind
  cd ikfast_pybind
  pip install .
```

## Adding new robots

### Docker workflow (recommended)

Using the Dockerfile and the library generation workflow in [pyikfast](https://github.com/cyberbotics/pyikfast), we can now (relatively) easily generate new ikfast modules for new robot models!

### Installing openrave from source

If you don't like docker and want to install openrave and ikfast manually, you can follow the instructions in [this tutorial](http://docs.ros.org/kinetic/api/framefab_irb6600_support/html/doc/ikfast_tutorial.html).
Warning: this can be non-trivial and time-consuming!

## Development


```
  # Building using Docker
  docker build . --tag pyikfast
  # replace ${PWD} with `pwd` if you are using bash
  docker run -it -v ${PWD}/output:/output --entrypoint bash pyikfast
```

## References

## Citation

If you find [IKFast](http://openrave.org/docs/0.8.2/openravepy/ikfast/) useful, 
please cite [OpenRave](http://openrave.org/):

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

## Related links

- [pyikfast](https://github.com/cyberbotics/pyikfast)
- [tutorial on ikfast cpp generation from a URDF (openrave installation from source)](http://docs.ros.org/kinetic/api/framefab_irb6600_support/html/doc/ikfast_tutorial.html).
- [ROS Answers: Generating an ikfast solution for 4 DOF arm](https://answers.ros.org/question/263925/generating-an-ikfast-solution-for-4-dof-arm/): a lot of useful links!