import rclpy    # the ROS 2 client library for Python
from rclpy.node import Node    # the ROS 2 Node class
import math
import numpy as np
import time
from mavros_msgs.msg import ManualControl
from sensor_msgs.msg import (FluidPressure as Pressure, Imu)
from std_msgs.msg import Float64
from ros2_auv_pid.pid import *


class MainMovement(Node):
    def __init__(self):
        super().__init__("main_publishing_node")

        # Variables
        self.depth = 0.0
        self.heading = 0.0
        self.surge = 0.0

        # Subscribers
        self.depth_subscription = self.create_subscription(Float64, "depth_control", self.depth_callback, 10)
        self.heading_subscription = self.create_subscription(Float64, "heading_control", self.heading_callback, 10)
        self.surge_subscription = self.create_subscription(Float64, "/surge_control", self.surge_callback, 10)

        # Publisher
        self.publish_movement_pid = self.create_publisher(ManualControl, '/manual_control', 10)

        # Publishing PID at 20 Hz
        self.timer = self.create_timer(0.05, self.publish_pid)


    def depth_callback(self, msg):
        self.depth = msg.data
    
    def heading_callback(self, msg):
        self.heading = msg.data

    def surge_callback(self, msg):
        self.surge = msg.data

    def publish_pid(self):
        msg = ManualControl()
        msg.x = min(max(self.surge, -500.0), 500.0)
        msg.y = 0.0
        msg.z = min(max(self.depth, -500.0), 500.0)
        if self.surge == 0:
            msg.r = min(max(self.heading, -500.0), 500.0)
        else:
            msg.r = min(max(self.heading, -500.0), 500.0)/5
        self.get_logger().info(f"New depth pid: {msg.z}") 
        self.get_logger().info(f"New heading pid: {msg.r}")

        self.publish_movement_pid.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = MainMovement()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt received, shutting down...")
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
