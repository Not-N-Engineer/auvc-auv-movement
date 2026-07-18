import rclpy    # the ROS 2 client library for Python
from rclpy.node import Node    # the ROS 2 Node class
import math
import time
from mavros_msgs.msg import ManualControl
from sensor_msgs.msg import (FluidPressure as Pressure,)
from ros2_auv_pid.pid import *


class DepthMovement(Node):
    def __init__(self):
        super().__init__("pid_node")

        #Variables
        self.z = None
        self.target_z = None
        self.previous_error = -1.0
        self.pid = 0.0
        self.dt = 0.05

        # Subscribers
        self.current_depth = self.create_subscription(Pressure, "pressure", self.current_depth_callback)
        # self.target_depth = self.create_subscription()

        # Publisher
        self.publish_depth_pid = self.create_publisher(ManualControl, '/manual_control', 10)

        # Publishing PID at 20 Hz
        self.timer = self.create_timer(self.dt, self.publish_pid)


    def current_depth_callback(self, msg):
        # Callback
        pressure = msg.fluid_pressure # kg / s^2 * m
        g = 9.81         # m / s^2
        density = 1000   # kg / m^3
        depth = pressure / (g * density) # m
        self.z = depth
        self.get_logger().info(f"New depth: {self.z}")

    def publish_pid(self):
        if not math.isclose(self.z, self.target_z, rel_tol=1e-05, abs_tol=0.0):
            # Calculating PID
            if self.previous_error == -1.0: self.previous_error = self.target_z - self.z
            self.pid, self.previous_error = pid(self.target_z, self.z, self.previous_error, self.dt)
            self.get_logger().info(f"New pid: {self.pid}")
            self.get_logger().info(f"New error: {self.previous_error}")

            msg = ManualControl()
            msg.x = 0.0
            msg.y = 0.0
            msg.z = self.pid
            msg.r = 0.0
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