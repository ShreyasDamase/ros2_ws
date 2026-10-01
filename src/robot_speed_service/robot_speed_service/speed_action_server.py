import time

import rclpy
from rclpy.node import Node
from robot_interface.action import SetRobotSpeedAction

from rclpy.action import ActionServer


class SpeedServer(Node):
    def __init__(self):
        super().__init__('speed_action_server_node')
        self.current_speed_ = 0.0
        self.action_server_ = ActionServer(
            self, SetRobotSpeedAction, 'set_robot_speed',
            self.execute_callback

        )
        self.get_logger().info("Robot speed action service started")

    def execute_callback(self, goal_handle):
        request = goal_handle.request
        feedback = SetRobotSpeedAction.Feedback()
        result = SetRobotSpeedAction.Result()

        start_speed = self.current_speed_
        target_speed = request.target_speed
        self.get_logger().info(
            f'request received goal:'
            f'target_speed = {target_speed}'
            f'gradual = {request.gradual}'
        )
        if request.gradual:
            steps = 10
            for i in range(1, steps + 1):
                if goal_handle.is_cancel_requested:
                    goal_handle.cancel()
                    result.success = False
                    result.applied_speed = self.current_speed_
                    result.message = 'Goal canceled'
                    return result

                progress = i / steps
                # new speed
                self.current_speed_ = (
                        start_speed + (target_speed - start_speed) * progress
                )

                # feedback
                feedback.current_speed = self.current_speed_
                feedback.progress = progress
                goal_handle.publish_feedback(feedback)
                self.get_logger().info(
                    f'speed :{self.current_speed_:.2f},'
                    f'progress :{progress * 100:.0f},'
                )
                time.sleep(0.5)
        else:
            self.current_speed_ = target_speed
            feedback.current_speed = self.current_speed_
            feedback.progress = 1.0
            goal_handle.publish_feedback(feedback)

        goal_handle.succeed()
        result.applied_speed = self.current_speed_
        result.success = True
        result.message = 'Speed applied successfully'
        self.get_logger().info(
            f'Goal completed'
            f'applied speed={self.current_speed_:.2f}'
        )
        return result


def main(args=None):
    rclpy.init(args=args)

    node = SpeedServer()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
