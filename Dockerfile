# # from https://github.com/cyberbotics/pyikfast
# FROM hamzamerzic/openrave

# RUN apt-get -y update && \
#   apt-get -y install lsb-core && \
#   sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list' && \
#   apt-key adv --keyserver 'hkp://keyserver.ubuntu.com:80' --recv-key C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654 && \
#   curl -sSL 'http://keyserver.ubuntu.com/pks/lookup?op=get&search=0xC1CF6E31E6BADE8868B172B4F42ED6FBAB17C654' | apt-key add - && \
#   apt-get -y update && \
#   apt install -y ros-kinetic-collada-urdf ros-kinetic-rosbash

# COPY entrypoint.bash /entrypoint.bash
# COPY src /src
# ENTRYPOINT ["/entrypoint.bash"]

# https://answers.ros.org/question/263925/generating-an-ikfast-solution-for-4-dof-arm/?answer=265625#post-id-265625
FROM personalrobotics/ros-openrave
RUN apt-get update || true && apt-get install -y --no-install-recommends build-essential python-pip liblapack-dev && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install sympy==0.7.1

ENTRYPOINT ["/ikfast_pybind/entrypoint.bash"]

# docker run -v ${PWD}:/ikfast_pybind personalrobotics/ros-openrave [base_link] [effector] [module_extension]