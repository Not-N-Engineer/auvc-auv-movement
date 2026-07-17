import rclpy    # the ROS 2 client library for Python
from rclpy.node import Node    # the ROS 2 Node class


class PID(Node):
    def __init__(self):
        super().__init__("pid_node")

        #Variables
        self.previous_error = -1.0

        #Publisher?


    #PID methods
    def p_control(self, desired_position, measured_position):
        Kp = 1.0
        error = desired_position - measured_position
        proportional = Kp * error
        return proportional
    
    def i_control(self, desired_position, measured_position, dt):
        Ki = 1.0
        error = desired_position - measured_position
        error_accumulator += error * dt # dt is the time since the last update
        integral = Ki * error_accumulator
        integral = min(Ki * error_accumulator, 1.0)
        return integral
    
    def d_control(self, desired_position, measured_position, dt):
        Kd = 1.0
        error = desired_position - measured_position
        if self.previous_error == -1.0: self.previous_error = error
        derivative = Kd * (error - self.previous_error) / dt # dt is the time since the last update
        self.previous_error = error
        return derivative



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