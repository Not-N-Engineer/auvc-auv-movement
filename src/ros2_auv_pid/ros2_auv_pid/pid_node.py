import rclpy    # the ROS 2 client library for Python
from rclpy.node import Node    # the ROS 2 Node class


class PID(Node):
    def __init__(self):
        super().__init__("pid_node")


def main(args=None):
    rclpy.init(args=args)
    node = PID()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt received, shutting down...")
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()