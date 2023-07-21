#!/bin/bash

URDF_FILE=${1}
BASE=${2}
EFFECTOR=${3}
EXTENSION=${4}

# Generate inverse kinematics files
cp /ikfast_pybind/data/${URDF_FILE} ${URDF_FILE}
source /opt/ros/kinetic/local_setup.bash
rosrun collada_urdf urdf_to_collada ${URDF_FILE} robot.dae
cat <<EOT >> robot.xml
<robot file="robot.dae">
  <Manipulator name="robot_workspace">
    <base>${BASE}</base>
    <effector>${EFFECTOR}</effector>
  </Manipulator>
</robot>
EOT

# [recommanded] let ikfast decides where to put the free joint
openrave.py --database inversekinematics --robot=robot.xml --iktype=transform6d --iktests=100

# [archived] specify the free joint
# python `openrave-config --python-dir`/openravepy/_openravepy_/ikfast.py --robot=robot.dae --iktype=transform6d --baselink=1 --eelink=9  --freeindex=4 --savefile=ikfast*.Transform6D.*.cpp

export NEW_IKMOD_DIR=/ikfast_pybind/src/${EXTENSION}

cp /src/_template ${NEW_IKMOD_DIR}

# `ikfast` generated files
cp $(find -name 'ikfast*.Transform6D.*.cpp') ${NEW_IKMOD_DIR}/ikfast_robot.cpp
cp $(find -name 'ikfast.h') ${NEW_IKMOD_DIR}/ikfast.h

sed -i "s/\[put_extension\]/${EXTENSION}/g" ${NEW_IKMOD_DIR}/CMakeLists.txt
sed -i "s/\[put_extension\]/${EXTENSION}/g" ${NEW_IKMOD_DIR}/ikfast_pybind_wrapper.cpp

# rename urdf for testing
mv ${URDF_FILE} ${EXTENSION}.urdf

# append "# ikfast" to the end of the CMakeLists.txt
cat <<EOT > src/CMakeLists.txt
add_subdirectory(${EXTENSION})
EOT