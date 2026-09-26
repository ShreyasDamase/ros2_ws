from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='parameter_pkg',
            executable='parameter',
            name='parameter_node',
            parameters=[{'robot_speed': 4.5}],
            output='screen'

        ),
        Node(
            package='parameter_pkg',
            executable='parameter_callback',
            name='parameter_callback_node',
            output='screen'

        )
    ])
