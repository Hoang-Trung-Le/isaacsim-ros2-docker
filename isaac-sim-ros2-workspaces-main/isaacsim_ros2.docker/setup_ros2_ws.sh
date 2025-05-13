#!/bin/bash
sudo rosdep fix-permissions
rosdep update
pip3 install Cython packaging pytest pytest-ros
source /opt/ros/humble/setup.sh
cd /ros2_ws
rosdep init
rosdep update
rosdep install --from-paths src --ignore-src -r -y
colcon build --cmake-args -DPython3_EXECUTABLE=/usr/bin/python3.10 --merge-install
export isaac_sim_package_path=/isaac-sim
export FASTRTPS_DEFAULT_PROFILES_FILE=/etc/fastdds.xml
export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
export ROS_DOMAIN_ID=24
source /ros2_ws/install/setup.sh
source /opt/ros/humble/setup.bash