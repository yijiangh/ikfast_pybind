# # from https://github.com/cyberbotics/pyikfast
# The older `hamzamerzic/openrave` image has become unreliable to pull from
# Docker Hub, so default to the still-published Personal Robotics image.
ARG OPENRAVE_BASE_IMAGE=personalrobotics/ros-openrave
FROM ${OPENRAVE_BASE_IMAGE}

ARG ROS_DISTRO=indigo
ENV ROS_DISTRO=${ROS_DISTRO}

RUN apt-get update && \
  apt-get install -y --allow-unauthenticated --no-install-recommends \
    build-essential \
    libblas-dev \
    liblapack-dev \
    python-pip \
    python-lxml \
    wget \
    "ros-${ROS_DISTRO}-collada-urdf" \
    "ros-${ROS_DISTRO}-rosbash" && \
  apt-get remove -y python-mpmath || true && \
  wget -O /tmp/sympy-0.7.1.tar.gz \
    https://files.pythonhosted.org/packages/0f/bc/104757e5baf262211bb42c10c404cb4912d206ddf596dd752ae0ae9e09ff/sympy-0.7.1.tar.gz && \
  cd /tmp && \
  tar -xzf sympy-0.7.1.tar.gz && \
  cd sympy-0.7.1 && \
  python setup.py install && \
  rm -rf /tmp/sympy-0.7.1 /tmp/sympy-0.7.1.tar.gz && \
  rm -rf /var/lib/apt/lists/*
  # apt-get -y install lsb-core && \
  # sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list' && \
  # apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654 && \
  # curl -sSL 'http://keyserver.ubuntu.com/pks/lookup?op=get&search=0xC1CF6E31E6BADE8868B172B4F42ED6FBAB17C654' | apt-key add - && \
  # apt-get -y update && \

RUN wget -O /usr/local/bin/round_collada_numbers.py \
  "https://raw.githubusercontent.com/ros-planning/moveit/${ROS_DISTRO}-devel/moveit_kinematics/ikfast_kinematics_plugin/scripts/round_collada_numbers.py"

COPY --chmod=755 entrypoint.bash /entrypoint.bash
ENTRYPOINT ["/entrypoint.bash"]

#####################

# https://answers.ros.org/question/263925/generating-an-ikfast-solution-for-4-dof-arm/?answer=265625#post-id-265625
# FROM personalrobotics/ros-openrave
# RUN apt-get update || true && apt-get install -y --no-install-recommends build-essential python-pip liblapack-dev && apt-get clean && rm -rf /var/lib/apt/lists/*
# # enforce a specific version of sympy, which is known to work with OpenRave
# # https://github.com/ros-planning/moveit/pull/2650
# # RUN pip install sympy==0.7.1
# RUN pip install git+https://github.com/sympy/sympy.git@sympy-0.7.1
# RUN  apt-get -y update && \
#   apt install -y wget ros-indigo-collada-urdf
# RUN wget https://raw.githubusercontent.com/ros-planning/moveit/indigo-devel/moveit_kinematics/ikfast_kinematics_plugin/scripts/round_collada_numbers.py

# RUN echo "source ${ROS_PREFIX_PATH}/setup.bash\n source ${ROS_WS_PATH}/install/setup.bash" >> ~/.bashrc

# ENTRYPOINT ["ikfast_pybind/entrypoint.bash"]

# docker run -v ${PWD}:/ikfast_pybind personalrobotics/ros-openrave [base_link] [effector] [module_extension]
# docker run -it --rm -v ${PWD}:/ikfast_pybind personalrobotics/ros-openrave
