import platform
import rclpy
from rclpy.node import Node

class PlatformNode(Node):
    def __init__(self):
        super().__init__('cross_platform_node')

        system_info = {
        'os':platform.system(),
        'releases':platform.release(),
        'architecture':platform.machine()
        }
        self.get_logger().info(
            f'Running on: {system_info}'
        )

def main():
    rclpy.init()
    node=PlatformNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__=='__main__':
    main()