import rclpy
from rclpy.executors import SingleThreadedExecutor
from rclpy.node import Node
import time


class ExecutionDemo(Node):
    def __init__(self):
        super().__init__('execution_demo_node')
        self.timer1_ = self.create_timer(1.0, self.timer_one_callback)

        self.timer1_ = self.create_timer(2.0, self.timer_two_callback)

    def timer_one_callback(self):
        self.get_logger().info('Timer 1 callback start')
        time.sleep(5)
        self.get_logger().info('Timer 1 callback finished')

    def timer_two_callback(self):
        self.get_logger().info('Timer 2 callback executed')


def main():
    rclpy.init()
    execution_demo = ExecutionDemo()
    executor = SingleThreadedExecutor()
    executor.add_node(execution_demo)
    try:
        # rclpy.spin(execution_demo)  # Single-threaded execution or you can write
        executor.spin()
    except KeyboardInterrupt:
        print('Process terminated with keyboard interrupt')
    finally:
        executor.shutdown()
        execution_demo.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
