import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64


class TalkerPublisherNode(Node):
    def __init__(self):
        super().__init__('talker_publisher_node')
        self.publisher_ = self.create_publisher(Int64, 'talker', 10)
        self.timer_ = self.create_timer(1.0, self.timer_callback)
        self.declare_parameter('count', 0)
        self.parameter_ = self.get_parameter('count')
        self.count = self.parameter_.value

    def timer_callback(self):
        msg = Int64()
        self.count += 1
        msg.data = self.count
        self.publisher_.publish( )
        self.get_logger().info(
            f'Publishing :{msg.data}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = TalkerPublisherNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
