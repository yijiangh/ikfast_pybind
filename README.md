
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

## Example use

```
# module is named as ikfast_[robot_extension_name]
from ikfast_abb_crb15000_5_95 import get_fk, get_ik, get_num_dofs, get_free_dofs

q = [-2.63657646 -0.0617853  -3.47712997  2.49898054 -2.52778128 -0.16582804]
position, rotation_matrix = get_fk(q)

# position: [0.26235064496283567, 0.14009087927384264, 0.4693020346263909]
# rotation_matrix: [[0.5406759469002327, -0.5079818162906635, -0.6705400769242471], [0.7000046675058794, 0.7137441604265776, 0.02372211893872128], [0.46654365917191476, -0.4822071627163975, 0.7414939421947302]]
# rotation matrix is represented as a list of row vectors

sols = get_ik(pos, rot)

# in this case, sols is a list of 6 solutions (number of solutions might vary, depending on the robot model and the end effector pose)
# sols = [[-2.677129219514031, -1.960941287457495, -0.01106834923090716, -1.5223522515329055, 2.9063099129126977, -0.38755718968184494], [-2.462522011120452, -1.849866796374988, -0.16773812158371804, 1.3011604100510745, -2.813500265809647, 2.6268679293971933], [0.5089732622755507, 1.9672642624270855, -2.814065035072528, 0.685267897567732, 2.7355477710862828, -1.3219543618811413], [0.6132567402414596, 1.8349107589147142, -2.3732420854723038, -2.683753814523185, -2.43160850087894, 1.6333350305270915], [-2.5541197756335254, -0.7657130735027564, -2.371472482718502, 0.303986095361348, -1.941822962815811, 1.3639870138920118], [-2.576171906556894, -0.38817105888328834, -2.8244159164056475, -2.8535006401539187, 1.8761237312641206, -1.823266925815287], [0.5794016926960825, 0.3881580373170367, 0.13744051886892136, 0.28233232570071304, 1.4356135803046326, -1.9377257941841823], [0.572866436900018, 0.7658018156114295, -0.30358025663392274, -2.863611514167973, -1.498111500637429, 1.215923255645185]]

```

## Adding new robots

### Docker workflow (recommended)

Using the Dockerfile and the library generation workflow in [pyikfast](https://github.com/cyberbotics/pyikfast), we can now (relatively) easily generate new ikfast modules for new robot models!

First, save your URDF file in the `data` folder (only the URDF suffices, meshes not needed), and then run the following command:

```
docker build . --tag openrave-ros-indigo
docker run -v ${PWD}:/ikfast_pybind openrave-ros-indigo [urdf_file_name] [base_link] [effector_link_name] [module_extension]
```

For example, for a `crb15000_5_95.urdf` file, we command:

```
docker run -v ${PWD}:/ikfast_pybind openrave-ros-indigo crb15000_5_95.urdf base_link tool0 abb_crb15000_5_95
```
And the resulting ikfast module will be named as `ikfast_abb_crb15000_5_95`.

After that, simply run `pip install .` to install the new module.

For testing, issue the following commands instead:

```
pip install . -r requirements-dev.txt
pytest tests/test_[module_extension].py
```

### Installing openrave from source

If you don't like docker and want to install openrave and ikfast manually, you can follow the instructions in [this tutorial](http://docs.ros.org/kinetic/api/framefab_irb6600_support/html/doc/ikfast_tutorial.html).
Warning: this can be non-trivial and time-consuming!

## Development


```
  # Building using Docker
  docker build . --tag openrave-ros-indigo
  # replace ${PWD} with `pwd` if you are using bash
  docker run -it -v ${PWD}:/ikfast_pybind --entrypoint bash openrave-ros-indigo
```

## TODO

- [ ] use github actions to build and test
- [ ] use github actions to test new model creation workflow

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