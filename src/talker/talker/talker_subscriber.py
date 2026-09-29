import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64


class TalkerSubscriber(Node):
    def __init__(self):
        super().__init__('talker_subscriber_node')
        self.subscription_ = self.create_subscription(Int64, 'talker', self.call_back, 10)

    def call_back(self, message: Int64):
        self.get_logger().info(
            f'Received value :{message.data}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = TalkerSubscriber()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
