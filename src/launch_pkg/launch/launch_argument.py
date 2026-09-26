from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.condition import Condition
from launch.actions import GroupAction
from launch.conditions import IfCondition


def generate_launch_description():
    robot_speed_arg = DeclareLaunchArgument(
        'robot_speed',
        default_value='2.0',
        description='Initial robot speed'

    )  # declare configural input

    enable_callback_arg = DeclareLaunchArgument(
        'enable_callback',
        default_value='true',
        description='Enable parameter callback'
    )
    enable_callback = LaunchConfiguration('enable_callback')
    robot_speed = LaunchConfiguration('robot_speed')  # retriv argument

    return LaunchDescription([
        robot_speed_arg,
        enable_callback_arg,
        Node(
            package='parameter_pkg',
            executable='parameter',
            name='parameter_node',
            namespace='robot1',
            condition=IfCondition(enable_callback),
            parameters=[{'robot_speed': robot_speed}],
            output='screen'

        ),
        Node(
            package='parameter_pkg',
            executable='parameter',
            name='parameter_node',
            namespace='robot2',
            parameters=[{'robot_speed': robot_speed}],
            output='screen'

        ),
        Node(
            package='parameter_pkg',
            executable='parameter_callback',
            name='parameter_callback_node',
            namespace='robot1',
            output='screen'

        )
    ])
