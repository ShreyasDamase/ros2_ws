import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from robot_interface.action import SetRobotSpeedAction


class SpeedClient(Node):
    def __init__(self):
        super().__init__('speed_action_client_node')
        self.action_client_ = ActionClient(self, SetRobotSpeedAction, 'set_robot_speed')

    def send_goal(self, target_speed, gradual):
        while not self.action_client_.wait_for_server(
                timeout_sec=1.0

        ):
            self.get_logger().info(
                'Waiting for action server...'
            )
        goal = SetRobotSpeedAction.Goal()
        goal.target_speed = target_speed
        goal.gradual = gradual

        self.get_logger().info(
            f'Sending goal: '
            f'target_speed={target_speed}, '
            f'gradual={gradual}'
        )

        future = self.action_client_.send_goal_async(goal, feedback_callback=self.feedback_callback)

        future.add_done_callback(
            self.goal_response_callback
        )

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(
            f'Feedback: '
            f'current_speed={feedback.current_speed:.2f}, '
            f'progress={feedback.progress * 100:.0f}%'
        )

    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().error(
                'Goal rejected'
            )

            return

        self.get_logger().info(
            'Goal accepted'
        )

        self.get_logger().info(
            f'Goal ID: {goal_handle.goal_id}'
        )

        # Ask for result
        result_future = goal_handle.get_result_async()

        result_future.add_done_callback(
            self.result_callback
        )

    def result_callback(self, future):
        result = future.result().result
        self.get_logger().info(
            f'Result received: '
            f'success={result.success}, '
            f'applied_speed={result.applied_speed:.2f}, '
            f'message="{result.message}"'
        )

        # Stop spinning after result
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)

    node = SpeedClient()

    node.send_goal(
        target_speed=100.0,
        gradual=True
    )

    rclpy.spin(node)

    node.destroy_node()


if __name__ == '__main__':
    main()
