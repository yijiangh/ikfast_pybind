#!/bin/bash
set -euo pipefail

URDF_FILE=${1}
BASE=${2}
EFFECTOR=${3}
EXTENSION=${4}
REPO_ROOT=/ikfast_pybind
export TMPDIR=${TMPDIR:-/tmp}

resolve_urdf_source() {
  if [[ -f "${URDF_FILE}" ]]; then
    printf '%s\n' "${URDF_FILE}"
    return 0
  fi

  if [[ -f "${REPO_ROOT}/data/${URDF_FILE}" ]]; then
    printf '%s\n' "${REPO_ROOT}/data/${URDF_FILE}"
    return 0
  fi

  echo "Unable to locate URDF file: ${URDF_FILE}" >&2
  return 1
}

ORIGINAL_URDF_SOURCE=$(resolve_urdf_source)
ORIGINAL_URDF_BASENAME=$(basename "${ORIGINAL_URDF_SOURCE}")
ORIGINAL_URDF_DIR=$(dirname "${ORIGINAL_URDF_SOURCE}")

# Stage the URDF and any sibling resources into a temporary working directory so
# relative mesh paths continue to resolve regardless of where the URDF came from.
WORKDIR=$(mktemp -d)
cp -r "${ORIGINAL_URDF_DIR}/." "${WORKDIR}/"
cd "${WORKDIR}"

setup_ros() {
  local candidates=()

  if [[ -n "${ROS_DISTRO:-}" ]]; then
    candidates+=("/opt/ros/${ROS_DISTRO}/local_setup.bash")
    candidates+=("/opt/ros/${ROS_DISTRO}/setup.bash")
  fi

  candidates+=("/opt/ros/kinetic/local_setup.bash")
  candidates+=("/opt/ros/kinetic/setup.bash")
  candidates+=("/opt/ros/indigo/local_setup.bash")
  candidates+=("/opt/ros/indigo/setup.bash")

  for candidate in "${candidates[@]}"; do
    if [[ -f "${candidate}" ]]; then
      local had_nounset=0
      if [[ -o nounset ]]; then
        had_nounset=1
        set +u
      fi

      # shellcheck disable=SC1090
      source "${candidate}"

      if [[ ${had_nounset} -eq 1 ]]; then
        set -u
      fi

      return 0
    fi
  done

  echo "Unable to find a ROS setup script under /opt/ros." >&2
  return 1
}

setup_ros
rosrun collada_urdf urdf_to_collada "${ORIGINAL_URDF_BASENAME}" robot.dae
python /usr/local/bin/round_collada_numbers.py robot.dae robot.rounded.dae 5
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
set +e
openrave0.9.py --database inversekinematics --robot=robot.xml --iktype=transform6d --iktests=100
OPENRAVE_STATUS=$?
set -e

IKFAST_SOURCE_FILE=$(find ~/.openrave/ -name 'ikfast*.Transform6D.*.cpp' -print -quit)
IKFAST_HEADER_FILE=$(find ~/.openrave/ -name 'ikfast.h' -print -quit)

if [[ ${OPENRAVE_STATUS} -ne 0 ]]; then
  if [[ -n "${IKFAST_SOURCE_FILE}" && -n "${IKFAST_HEADER_FILE}" ]]; then
    echo "OpenRAVE self-test failed after generating IKFast sources; continuing with generated files." >&2
  else
    exit "${OPENRAVE_STATUS}"
  fi
fi

# [archived] specify the free joint
# python `openrave-config --python-dir`/openravepy/_openravepy_/ikfast.py --robot=robot.dae --iktype=transform6d --baselink=1 --eelink=9  --freeindex=4 --savefile=ikfast*.Transform6D.*.cpp

NEW_IKMOD_DIR=${REPO_ROOT}/src/${EXTENSION}

mkdir -p "${NEW_IKMOD_DIR}"
cp "${REPO_ROOT}/src/_template/CMakeLists.txt" "${NEW_IKMOD_DIR}/CMakeLists.txt"
cp "${REPO_ROOT}/src/_template/ikfast_pybind_wrapper.cpp" "${NEW_IKMOD_DIR}/ikfast_pybind_wrapper.cpp"
cp "${REPO_ROOT}/src/_template/test_[put_extension].py" "${NEW_IKMOD_DIR}/test_[put_extension].py"

# `ikfast` generated files
cp "${IKFAST_SOURCE_FILE}" ${NEW_IKMOD_DIR}/ikfast_source.cpp
cp "${IKFAST_HEADER_FILE}" ${NEW_IKMOD_DIR}/ikfast.h

sed -i "s/\[put_extension\]/${EXTENSION}/g" ${NEW_IKMOD_DIR}/CMakeLists.txt
sed -i "s/\[put_extension\]/${EXTENSION}/g" ${NEW_IKMOD_DIR}/ikfast_pybind_wrapper.cpp
sed -i "s/\[put_extension\]/${EXTENSION}/g" ${NEW_IKMOD_DIR}/test_[put_extension].py

sed -i 's!#define IKFAST_COMPILE!// #define IKFAST_COMPILE!g' ${NEW_IKMOD_DIR}/ikfast_source.cpp
sed -i 's!IKFAST_COMPILE_ASSERT(IKFAST!// IKFAST_COMPILE_ASSERT(IKFAST!g' ${NEW_IKMOD_DIR}/ikfast_source.cpp
sed -i 's/isnan _isnan/isnan std::isnan/g' ${NEW_IKMOD_DIR}/ikfast_source.cpp
sed -i 's/isinf _isinf/isinf std::isinf/g' ${NEW_IKMOD_DIR}/ikfast_source.cpp

# move test file rename urdf for testing
mv -f ${NEW_IKMOD_DIR}/test_[put_extension].py ${REPO_ROOT}/tests/test_${EXTENSION}.py
cp "${ORIGINAL_URDF_BASENAME}" ${REPO_ROOT}/data/${EXTENSION}.urdf

# append "# ikfast" to the end of the CMakeLists.txt
if ! grep -Fxq "add_subdirectory(${EXTENSION})" "${REPO_ROOT}/src/CMakeLists.txt"; then
cat <<EOT >> ${REPO_ROOT}/src/CMakeLists.txt

add_subdirectory(${EXTENSION})
EOT
fi
