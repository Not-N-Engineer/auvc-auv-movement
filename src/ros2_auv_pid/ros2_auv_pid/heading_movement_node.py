import rclpy    # the ROS 2 client library for Python
from rclpy.node import Node    # the ROS 2 Node class
import math
import numpy as np
import time
from mavros_msgs.msg import ManualControl
from sensor_msgs.msg import (FluidPressure as Pressure, Imu)
from std_msgs.msg import Float64
from ros2_auv_pid.pid import *


class HeadingMovement(Node):
    def __init__(self):
        super().__init__("heading_node")

        # Variables
        self.r = 0.0
        self.target_r = np.pi
        self.previous_error = -1.0
        self.error_acc = 0
        self.pid = 0.0
        self.dt = 0.05

        # Subscribers
        self.current_heading = self.create_subscription(Imu, "imu", self.current_heading_callback, 10)
        self.target_heading = self.create_subscription(Float64, "/target_heading", self.target_heading_callback, 10)

        # Publisher
        self.publish_heading_pid = self.create_publisher(Float64, 'heading_control', 10)

        # Publishing PID at 20 Hz
        self.timer = self.create_timer(self.dt, self.publish_pid)


    def target_heading_callback(self, msg):
        self.target_r = msg.data
        self.get_logger().info(f"NEW TARGET HEADING: {self.target_r}") 

    def current_heading_callback(self, msg):
        # Callback
        rotation_v = msg.zgyro
        heading = self.r + rotation_v
        
        self.r = heading
        self.get_logger().info(f"New heading: {self.r}")

    def publish_pid(self):
        if not self.r == self.target_r:
            # Calculating PID
            if self.previous_error == -1.0: self.previous_error = self.target_r - self.r
            self.pid, self.previous_error = pid(self.target_r, self.r, self.previous_error, self.error_acc, self.dt, 3.6, 0.0, 1.2)
            self.error_acc = self.previous_error * self.dt
            self.get_logger().info(f"New pid: {self.pid}")
            self.get_logger().info(f"New error: {self.previous_error}")

            msg = Float64()
            msg.data = max(self.pid * -83.3, -500.0)
            self.publish_depth_pid.publish(msg)
            self.get_logger().info(f"Target Depth: {self.target_r}")
            self.get_logger().info(f"Current Depth: {self.r}")


def main(args=None):
    rclpy.init(args=args)
    node = HeadingMovement()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt received, shutting down...")
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()