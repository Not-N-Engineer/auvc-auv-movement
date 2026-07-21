**SITL:**  
~/ardupilot/Tools/autotest/sim_vehicle.py --vehicle=ArduSub --aircraft="bwsibot" -L RATBeach --out=udp:192.168.3.1:14550  

  
**Rosmav build:**  
cd ~/auvc-auv-movement && colcon build --packages-select rosmav && source install/setup.zsh  
**Rosmav run:**  
ros2 run rosmav bluerov2_hardware_interface  

  
**Nodes build:**  
cd ~/auvc-auv-movement && colcon build --packages-select ros2_auv_pid && source install/setup.zsh  
  
**All nodes run:**  
ros2 launch ros2_auv_pid pid.launch.yaml  
ros2 run ros2_auv_pid depth_movement_node  
ros2 run ros2_auv_pid heading_movement_node  
ros2 run ros2_auv_pid movement_publisher_node  
  
  
**Arm**  
ros2 service call /arming std_srvs/srv/SetBool "{data: true}"  
ros2 service call /arming std_srvs/srv/SetBool "{data: false}"  


**New Target Depth**  
ros2 topic pub --once /target_depth std_msgs/msg/Float64 "{data: 1.0}"
ros2 topic pub --once /target_heading std_msgs/msg/Float64 "{data: 135.0}"
ros2 topic pub --once /surge_control std_msgs/msg/Float64 "{data: 250.0}"
