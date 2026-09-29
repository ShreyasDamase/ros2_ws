from robot_interface.srv import SetRobotSpeed
import rclpy
from rclpy.node import Node


class RobotSpeedServer(Node):
    def __init__(self):
        super().__init__('robot_speed_server')
        # current speed
        self.current_speed_ = 0.0
        # max speed limit
        self.max_speed_ = 10.0
        # create service
        self.service_ = self.create_service(
            SetRobotSpeed,
            'speed',
            self.set_robot_speed_callback
        )
        self.get_logger().info("Robot server is ready")

    def set_robot_speed_callback(self, request, response):
        self.get_logger().info(
            f'Request received with:'
            f'Requested speed: {request.target_speed:.2f}'
            f'gradual flag: {request.gradual}'
        )

        if request.target_speed < 0.0:
            response.success = False
            response.applied_speed = self.current_speed_
            response.message = 'Target speed can not be negative'
            return response

        if request.target_speed > 10.0:
            response.success = False
            response.applied_speed = self.current_speed_
            response.message = 'Target speed can not be more than 10.00'
            return response

        if request.gradual:
            self.get_logger().info('Gradual speed transition required')
        else:
            self.get_logger().info('Immediate speed transition required')

        self.current_speed_ = request.target_speed
        response.applied_speed = self.current_speed_
        response.success = True
        response.message = 'Speed update successfully'
        return response


def main(args=None):
    rclpy.init(args=args)
    node = RobotSpeedServer()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print('program terminated with keyboard interrupt')
    finally:
        node.destroy_node()
        rclpy.shutdown()
