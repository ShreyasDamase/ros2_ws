import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from rcl_interfaces.msg import SetParametersResult


class ParameterCallback(Node):
    def __init__(self):
        super().__init__('parameter_callback_node')
        self.declare_parameter('robot_speed', 2.0)
        self.add_on_set_parameters_callback(self.parameter_callback)

    def parameter_callback(self, params):
        for param in params:
            if param.name == 'robot_speed' and param.type_ == Parameter.Type.DOUBLE:

                if param.value < 0.0 or param.value > 5.0:
                    self.get_logger().info(
                        f'Invalid parameter must be between 0.0<= value <=5.0  '
                    )
                    return SetParametersResult(successful=False,
                                               reason='Invalid parameter must be between 0.0<= value <=5.0 ')

                self.get_logger().info(
                    f'parameter for parameter_callback_node changed as {param.name}: {param.value} '
                )
                return SetParametersResult(successful=True)

        self.get_logger().info(
            f'Invalid parameter type'
        )

        return SetParametersResult(successful=False, reason='Invalid parameter must be between 0.0<= value <=5.0 ')


def main(args=None):
    rclpy.init(args=args)
    node = ParameterCallback()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Node stopped by Ctrl+C')
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
