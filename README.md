
# ikfast_pybind

[![Github Actions Build Status](https://github.com/yslbit/ikfast_pybind_aubo/workflows/build/badge.svg)](https://github.com/yslbit/ikfast_pybind_aubo/actions)
[![License](https://img.shields.io/github/license/yslbit/ikfast_pybind_aubo.svg)](https://github.com/yslbit/ikfast_pybind_aubo/blob/main/LICENSE)

**ikfast_pybind** is a python binding generation library for the analytic kinematics engine [IKfast](http://openrave.org/docs/1.8.2/openravepy/ikfast/). 
The python bindings are generated via [pybind11](https://github.com/pybind/pybind11) a [CMake](https://cmake.org/)-based build system.

## Main features

Analytical inverse and forward kinematics (IK and FK) for robots with **less or equal than six degrees of freedom**. 
For a given end effector pose, ikfast computes **all** IK solutions (e.g. 8 solutions for a 6-dof robot).
The ikfast backend is C++ code, and it only performs geometric kinematic computations, it is fast and deterministic.

However, **ikfast knows nothing about the robot's joint limits and collision models**, so it is up to the user to filter the solutions and check for collisions.

**Note:** 
This repository focuses on the `aubo_i3H` IKFast generation workflow.
It includes the generated IKFast C++ source, the pybind11 wrapper, and the build scripts needed to compile the Python module.

The actual IKFast C++ code generation is done by OpenRAVE's `ikfast` module.
This repository documents the `aubo_i3H` workflow in the [Generating `aubo_i3H` with Docker](#generating-aubo_i3h-with-docker) section.

If you want to add a new robot, start from the `yh/add_robot_from_docker` branch.

## Installation

### Prerequisites for Windows

We ONLY support installing from **conda** on Windows (pip not supported).

Make sure you **uninstall `numpy` that is installed via `pip`**, and then install `numpy` via `conda`.

```bash
conda install numpy==1.21.5 mkl-devel cmake
```

<details>
  <summary>Click for reasons</summary>

This is because some ikfast module needs lapack C routines, and we rely on `numpy` and `mkl-devel` to link the correct lapack library.

From [this post](https://github.com/primme/primme/issues/37#issuecomment-692066436):
> The Windows' numpy version on pypi is shipped with OpenBLAS dlls, but not the lib files required by the linker. The errors showed on previous comments came from the linker (error LNKXXXX).
</details>

### Package installation

```
  git clone --recursive https://github.com/yslbit/ikfast_pybind_aubo.git
  cd ikfast_pybind_aubo
  pip install .
```

## Example use

```
# module is named as ikfast_aubo_i3H
from ikfast_aubo_i3H import get_fk, get_ik, get_num_dofs, get_free_dofs

q = [0.0] * get_num_dofs()
position, rotation_matrix = get_fk(q)

free_jt_values = [0.0 for _ in get_free_dofs()] 
sols = get_ik(position, rotation_matrix, free_jt_values)
```

## Generating `aubo_i3H` with Docker

This repository focuses on generating the IKFast module for `aubo_i3H`.

### 1. Download the input files into `data/aubo_i3H`

Create the following directory layout inside this repository:

```text
data/
  aubo_i3H/
    aubo_i3H.urdf
    meshes/
      visual/
        link0.DAE
        link1.DAE
        link2.DAE
        link3.DAE
        link4.DAE
        link5.DAE
        link6.DAE
      collision/
        link0.STL
        link1.STL
        link2.STL
        link3.STL
        link4.STL
        link5.STL
        link6.STL
```

The URDF should stay at:

```bash
data/aubo_i3H/aubo_i3H.urdf
```

The mesh files must keep the same relative paths used by the URDF, so keep the `meshes/visual` and `meshes/collision` folders beside it.

### 2. Build the Docker image

Build the generator image from the repository root:

```bash
docker build . --tag openrave-ros-indigo
```

The image includes the compatibility fixes required by this legacy OpenRAVE workflow:

- `sympy==0.7.1`
- `python-lxml`
- `build-essential`
- `libblas-dev`
- `liblapack-dev`

### 3. Generate the `aubo_i3H` IKFast sources

The `aubo_i3H` kinematic chain uses:

- `base_link` as the base link
- `wrist3_Link` as the end-effector link
- `aubo_i3H` as the module extension name

Run:

```bash
docker run --rm \
  -e TMPDIR=/tmp \
  -v ${PWD}:/ikfast_pybind \
  openrave-ros-indigo \
  aubo_i3H/aubo_i3H.urdf \
  base_link \
  wrist3_Link \
  aubo_i3H
```

### 4. Check the generated files

After the command finishes, the repository should contain:

```text
src/aubo_i3H/
data/aubo_i3H.urdf
tests/test_aubo_i3H.py
```

If Docker writes the generated files back as `root` or `nobody`, fix ownership before editing them locally:

```bash
sudo chown -R $USER:$USER src/aubo_i3H data/aubo_i3H.urdf tests/test_aubo_i3H.py
```

### 5. Install and test

Install the generated module:

```bash
pip install .
```

For testing:

```bash
pip install -r requirements-dev.txt
pytest tests/test_aubo_i3H.py
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
