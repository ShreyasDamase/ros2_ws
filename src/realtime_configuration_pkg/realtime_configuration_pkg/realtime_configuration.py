import rclpy
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
from rclpy.qos import (
QoSProfile,
QoSReliabilityPolicy,
QoSHistoryPolicy
)
from std_msgs.msg import String
class RealTimeNode(Node):
    def __init__(self):
        super().__init__('realtime_node')
        qos_profile=QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=1
        )
        self.subscription =self.create_subscription(String,'realtime_topic',self.realtime_callback,qos_profile)

    def realtime_callback(self,msg):
        self.get_logger().info(
            f'Realtime processing: {msg.data}'
        )

def main(args=None):
    rclpy.init(args=args)
    node=RealTimeNode()
    executor = SingleThreadedExecutor()
    executor.add_node(node)
    executor.spin()


if __name__ == '__main__':
    main()