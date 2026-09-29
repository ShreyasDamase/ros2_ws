import time

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class TurtleControlNode(Node):
    def __init__(self):
        super().__init__('turtle_cntrole_node')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.timer_ = self.create_timer(1.0, self.publish_velocity)
        self.get_logger().info('Turtle control node has started')

    def publish_velocity(self):
        msg = Twist()
        msg.linear.x = 2.1
        msg.angular.z = 2.1
        self.publisher_.publish(msg)
        self.get_logger().info(
            f'Published velocity with linear.x: {msg.linear.x}, angular: {msg.angular.z} '
        )
        time.sleep(3)


def main():
    rclpy.init()
    node = TurtleControlNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print('Program terminated due to keyboard Interrupt')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
