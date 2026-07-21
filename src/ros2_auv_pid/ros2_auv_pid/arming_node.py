import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool

class Arm(Node):
    def __init__(self):
        super().__init__('arming_node')

        # Initialize the ROS2 Client targeting MAVROS
        self.arm_client = self.create_client(SetBool, '/arming')
        
        # Wait until the MAVROS arming service is up and running
        while not self.arm_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /mavros/cmd/arming service to become available...')

        # Trigger the arming function once after 2 seconds
        self.timer = self.create_timer(2.0, self.arm_vehicle)
        
    def arm_vehicle(self):
        # Cancel the timer so we don't spam arming requests every 2 seconds
        self.timer.cancel()

        # Create the request payload
        request = SetBool.Request()
        request.data = True  # True to ARM, False to DISARM

        self.get_logger().info("Sending arming request...")
        future = self.arm_client.call_async(request)
        
        # Add a callback to handle the response safely without blocking the execution thread
        future.add_done_callback(self.arm_callback)

    def arm_callback(self, future):
        try:
            response = future.result()
            if response.success:
                self.get_logger().info("Vehicle ARMED successfully!")
            else:
                self.get_logger().error(f"Failed to arm vehicle: {response.result}")
        except Exception as e:
            self.get_logger().error(f"Service call failed: {e}")


def main(args=None):
    rclpy.init(args=args)
    node = Arm()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("\nShutting down safely...")
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
