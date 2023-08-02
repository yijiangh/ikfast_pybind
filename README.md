
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

### For Windows

Make sure you uninstall `numpy` that is installed via `pip`, and then install `numpy` via `conda`.
This is because some ikfast module needs lapack C routines, and we rely on `numpy` and `mkl-devel` to link the correct lapack library.

From [this post](https://github.com/primme/primme/issues/37#issuecomment-692066436):
> The Windows' numpy version on pypi is shipped with OpenBLAS dlls, but not the lib files required by the linker. The errors showed on previous comments came from the linker (error LNKXXXX).

```bash
conda install numpy==1.21.5 mkl-devel
```

### Package installation

```
  git clone --recursive https://github.com/yijiangh/ikfast_pybind
  cd ikfast_pybind
  pip install .
```

## Example use

```
# module is named as ikfast_[robot_extension_name]
from ikfast_abb_crb15000_5_95 import get_fk, get_ik, get_num_dofs, get_free_dofs

q = [-2.63657646, -0.0617853, -3.47712997, 2.49898054, -2.52778128, -0.16582804]
position, rotation_matrix = get_fk(q)

# position: [0.26235064496283567, 0.14009087927384264, 0.4693020346263909]
# rotation_matrix: [[0.5406759469002327, -0.5079818162906635, -0.6705400769242471], [0.7000046675058794, 0.7137441604265776, 0.02372211893872128], [0.46654365917191476, -0.4822071627163975, 0.7414939421947302]]
# rotation matrix is represented as a list of row vectors

free_jt_values = [0.0 for _ in get_free_dofs()] 
sols = get_ik(position, rotation_matrix, free_jt_values)

# in this case, sols is a list of 6 solutions (number of solutions might vary, depending on the robot model and the end effector pose)
# sols = [[0.1785012616767494, -0.06199018233064224, 0.9436855502338978, 1.3325306149957543, 2.9945201652283844, 1.972264584727056], [-2.8723216577666806, 0.07706247653191295, 2.4859280781704323, -0.6391567407014379, 2.797466174104682, 3.1039525057376918], [0.595183983463263, 0.04638407172278151, 0.9972710436611631, -1.8073165482899924, -2.722515509853957, -1.5229800022737439], [-2.6365764600000077, -0.061785300000067114, 2.80605533717965, 2.498980539999991, -2.5277812799999997, -0.1658280399999971], [0.3664639454322902, 2.292030718140481, 2.8234779285018097, -0.2965154649191957, -1.115407403792898, 0.6302298067592147], [0.4262690963574123, 2.671934012447336, 2.473145865089277, 2.805800126894165, 1.1359578012309193, -2.547101913122589], [-2.813459022748522, -2.292502631009238, 0.7896485486038122, 2.7485290573391628, -0.6723531017436907, 0.8406712722839281], [-2.6627850700615348, -2.6707543898059822, 1.1132893418128118, -0.5215490614298172, 0.7239187102366416, -2.329787315858479]]
```

## Adding new robots

### Docker workflow (recommended)

Using the Dockerfile and the library generation workflow in [pyikfast](https://github.com/cyberbotics/pyikfast), we can now (relatively) easily generate new ikfast modules for new robot models!

First, save your URDF file in the `data` folder (only the URDF suffices, meshes not needed), and then run the following command:

```
docker build . --tag openrave-ros-indigo
docker run -v ${PWD}:/ikfast_pybind openrave-ros-indigo [urdf_file_name] [base_link] [effector_link_name] [module_extension]
```

TODO:
kuka_kr6_r900.urdf robot_base_link robot_tool0 kr6_r900_6b

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

TODO

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