import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class VelocitySubscriber(Node):
    def __init__(self):
        super().__init__('velocity_subscriber_node')
        self.subscription = self.create_subscription(Float32, 'velocity', self.on_velocity, 10)

    def on_velocity(self, speed: Float32):
        self.get_logger().info(
            f'received velocity : {speed.data} '
        )


def main(args=None):
    rclpy.init(args=args)
    velocity_subscriber = VelocitySubscriber()
    try:
        rclpy.spin(velocity_subscriber)
    except KeyboardInterrupt:
        velocity_subscriber.get_logger().error('Code exit with keyboard interrupt')
    finally:
        velocity_subscriber.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
