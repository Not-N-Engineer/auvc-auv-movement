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

        # Subscribers
        self.depth = self.create_subscription(ManualControl, "depth_control", self.depth_callback, 10)
        self.heading = self.create_subscription(ManualControl, "heading_control", self.heading_callback, 10)

        # Publisher
        self.publish_pid = self.create_publisher(ManualControl, '/manual_control', 10)

        # Publishing PID at 20 Hz
        self.timer = self.create_timer(self.dt, self.publish_pid)


    def depth_callback(self, msg):
        self.depth = msg.data
        self.get_logger().info(f"New depth: {self.depth}") 

    def heading_callback(self, msg):
        self.heading = msg.data
        self.get_logger().info(f"New heading: {self.heading}")

    def publish_pid(self):
        msg = ManualControl()
        msg.x = 0.0
        msg.y = 0.0
        msg.z = self.depth
        msg.r = self.heading


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