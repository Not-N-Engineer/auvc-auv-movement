import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool
from pymavlink import mavutil
from mavros_msgs.msg import OverrideRCIn, ManualControl

class Arm(Node):
    def __init__(self):
        super().__init__("arming_node")
        self.mavlink.arducopter_arm()
        self.get_logger().info("AUV armed")

def main(args=None):
    rclpy.init(args=args)
    node = Arm()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node._set_neutral_all_channels()
        node.mavlink.arducopter_disarm()
        print("\nKeyboardInterrupt received, shutting down...")
        print("\nAUV disarmed")
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()