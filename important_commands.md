**SITL:**
~/ardupilot/Tools/autotest/sim_vehicle.py --vehicle=ArduSub --aircraft="bwsibot" -L RATBeach --out=udp:192.168.3.1:14550


**Rosmav build:**
cd ~/auvc-auv-movement && colcon build --packages-select rosmav && source install/setup.zsh

**Rosmav run:**
ros2 run rosmav bluerov2_hardware_interface


**Nodes build:**
cd ~/auvc-auv-movement && colcon build --packages-select ros2_auv_pid && source install/setup.zsh

**Depth node run:**
ros2 run ros2_auv_pid depth_movement_node
