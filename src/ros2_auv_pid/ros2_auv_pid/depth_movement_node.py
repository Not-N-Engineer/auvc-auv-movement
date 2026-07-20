import rclpy    # the ROS 2 client library for Python
from rclpy.node import Node    # the ROS 2 Node class
import math
import time
from mavros_msgs.msg import ManualControl
from sensor_msgs.msg import (FluidPressure as Pressure,)
from std_msgs.msg import Float64
from ros2_auv_pid.pid import *


class DepthMovement(Node):
    def __init__(self):
        super().__init__("depth_node")

        # Variables
        self.z = 0
        self.target_z = 2.5
        self.previous_error = -1.0
        self.error_acc = 0
        self.pid = 0.0
        self.dt = 0.05

        # Subscribers
        self.current_depth = self.create_subscription(Pressure, "pressure", self.current_depth_callback, 10)
        self.target_depth = self.create_subscription(Float64, "/target_depth", self.target_depth_callback, 10)

        # Publisher
        self.publish_depth_pid = self.create_publisher(Float64, 'depth_control', 10)

        # Publishing PID at 20 Hz
        self.timer = self.create_timer(self.dt, self.publish_pid)


    def target_depth_callback(self, msg):
        self.target_z = msg.data
        self.get_logger().info(f"NEW TARGET DEPTH: {self.target_z}") 

    def current_depth_callback(self, msg):
        # Callback
        pressure = msg.fluid_pressure - 101325 # kg / s^2 * m
        g = 9.81         # m / s^2
        density = 1000   # kg / m^3
        depth = pressure / (g * density) # m
        self.z = depth
        self.get_logger().info(f"New depth: {self.z}")

    def publish_pid(self):
        if not self.z == self.target_z:
            # Calculating PID
            if self.previous_error == -1.0: self.previous_error = self.target_z - self.z
            self.pid, self.previous_error = pid(self.target_z, self.z, self.previous_error, self.error_acc, self.dt, 3.6, 0.0, 1.2)
            self.error_acc = self.previous_error * self.dt
            self.get_logger().info(f"New pid: {self.pid}")
            self.get_logger().info(f"New error: {self.previous_error}")

            msg = Float64()
            msg.data = max(self.pid * -83.3, -500.0)
            self.publish_depth_pid.publish(msg)
            self.get_logger().info(f"Target Depth: {self.target_z}")
            self.get_logger().info(f"Current Depth: {self.z}")


def main(args=None):
    rclpy.init(args=args)
    node = DepthMovement()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt received, shutting down...")
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()