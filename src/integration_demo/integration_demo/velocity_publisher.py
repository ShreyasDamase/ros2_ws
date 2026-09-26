import rclpy
from rcl_interfaces import msg
from rclpy.node import Node
from std_msgs.msg import Float32
from rcl_interfaces.msg import SetParametersResult


class VelocityPublisher(Node):
    def __init__(self):
        super().__init__('velocity_publisher_node')
        self.declare_parameter('robot_speed', 1.0)
        self.robot_speed = self.get_parameter('robot_speed').value
        self.add_on_set_parameters_callback(self.parameter_callback)
        self.publisher_ = self.create_publisher(Float32, 'velocity', 10)
        self.timer = self.create_timer(1.0, self.publish_velocity_callback)

    def parameter_callback(self, params):
        for param in params:
            if param.name == 'robot_speed':
                if param.value < 0.0 or param.value > 10.0:
                    self.get_logger().error('robot speed can not be set negative or more than 10.0')
                    return SetParametersResult(successful=False)
                else:
                    return SetParametersResult(successful=True)
        self.get_logger().error('Invalid argument please enter correct robot speed ')
        return SetParametersResult(successful=False)

    def publish_velocity_callback(self):
        msg = Float32()
        if self.robot_speed is not None:
            msg.data = float(self.robot_speed)
        else:
            self.get_logger().warn('robot speed is none')
            return
        self.publisher_.publish(msg)
        self.get_logger().info(
            f'Publish velocity is :{msg.data}'
        )


def main(args=None):
    rclpy.init(args=args)
    velocity_publisher = VelocityPublisher()
    try:
        rclpy.spin(velocity_publisher)
    except KeyboardInterrupt:
        velocity_publisher.get_logger().error('Code exit with keyboard interrupt')
    finally:
        velocity_publisher.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
