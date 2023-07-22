#!/bin/bash

URDF_FILE=${1}
BASE=${2}
EFFECTOR=${3}
EXTENSION=${4}

# Generate inverse kinematics files
cp /ikfast_pybind/data/${URDF_FILE} ${URDF_FILE}
./ros_entrypoint.sh
rosrun collada_urdf urdf_to_collada ${URDF_FILE} robot.dae
python round_collada_numbers.py robot.dae robot.rounded.dae 5
cat <<EOT > robot.xml
<robot file="robot.rounded.dae">
  <Manipulator name="robot_workspace">
    <base>${BASE}</base>
    <effector>${EFFECTOR}</effector>
  </Manipulator>
</robot>
EOT

# [recommanded] let ikfast decides where to put the free joint
# clean up all previously generated ikfast files
rm -rf ~/.openrave/*
openrave0.9.py --database inversekinematics --robot=robot.xml --iktype=transform6d --iktests=100

# [archived] specify the free joint
# python `openrave-config --python-dir`/openravepy/_openravepy_/ikfast.py --robot=robot.dae --iktype=transform6d --baselink=1 --eelink=9  --freeindex=4 --savefile=ikfast*.Transform6D.*.cpp

NEW_IKMOD_DIR=/ikfast_pybind/src/${EXTENSION}

cp -r /ikfast_pybind/src/_template ${NEW_IKMOD_DIR}

# `ikfast` generated files
cp $(find ~/.openrave/ -name 'ikfast*.Transform6D.*.cpp') ${NEW_IKMOD_DIR}/ikfast_source.cpp
cp $(find ~/.openrave/ -name 'ikfast.h') ${NEW_IKMOD_DIR}/ikfast.h

sed -i "s/\[put_extension\]/${EXTENSION}/g" ${NEW_IKMOD_DIR}/CMakeLists.txt
sed -i "s/\[put_extension\]/${EXTENSION}/g" ${NEW_IKMOD_DIR}/ikfast_pybind_wrapper.cpp
sed -i "s/\[put_extension\]/${EXTENSION}/g" ${NEW_IKMOD_DIR}/test_[put_extension].py

sed -i 's!#define IKFAST_COMPILE!// #define IKFAST_COMPILE!g' ${NEW_IKMOD_DIR}/ikfast_source.cpp
sed -i 's!IKFAST_COMPILE_ASSERT(IKFAST!// IKFAST_COMPILE_ASSERT(IKFAST!g' ${NEW_IKMOD_DIR}/ikfast_source.cpp
sed -i 's/isnan _isnan/isnan std::isnan/g' ${NEW_IKMOD_DIR}/ikfast_source.cpp
sed -i 's/isinf _isinf/isinf std::isinf/g' ${NEW_IKMOD_DIR}/ikfast_source.cpp

# move test file rename urdf for testing
mv ${NEW_IKMOD_DIR}/test_[put_extension].py /ikfast_pybind/tests/test_${EXTENSION}.py
mv ${URDF_FILE} /ikfast_pybind/data/${EXTENSION}.urdf

# append "# ikfast" to the end of the CMakeLists.txt
cat <<EOT >> /ikfast_pybind/src/CMakeLists.txt

add_subdirectory(${EXTENSION})
EOT