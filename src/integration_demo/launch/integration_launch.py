import os.path

from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution

import os


def generate_launch_description():
    #1st way to get absolute path of yml
    config_file = PathJoinSubstitution([
        FindPackageShare('integration_demo'),
        'config',
        'velocity_params.yml'
    ])
    #2nd way to get absolute path of yml which required datafile registry inside setup.py
    pkg_share = get_package_share_directory('integration_demo')
    velocity_param_file = os.path.join(pkg_share, 'config', 'velocity_params.yml')

    robot_speed_arg = DeclareLaunchArgument(
        'robot_speed',
        default_value='1.0',
        description='Initial speed of the robot'
    )

    robot_speed = LaunchConfiguration('robot_speed')
    return LaunchDescription([
        robot_speed_arg,
        Node(
            package='integration_demo',
            executable='velocity_publisher',
            namespace='robot1',
            name='velocity_publisher_node',
            # parameters=[{'robot_speed': robot_speed}],
            # parameters=[
            #     '/Users/shreyasdamase/Terminator/ROS2_PROJECTS/ros2_ws/src/integration_demo/config/velocity_params.yml'],
            parameters=[velocity_param_file],
            output='screen'
        ),
        Node(
            package='integration_demo',
            executable='velocity_publisher',
            namespace='robot2',
            name='velocity_publisher_node',
            # parameters=[{'robot_speed': robot_speed}],
            # parameters=[
            #     '/Users/shreyasdamase/Terminator/ROS2_PROJECTS/ros2_ws/src/integration_demo/config/velocity_params.yml'],
            parameters=[config_file],
            output='screen'
        ),
        Node(
            package='integration_demo',
            executable='velocity_subscriber',
            namespace='robot1',
            name='velocity_subscriber_node',
            output='screen'
        ),
        Node(
            package='integration_demo',
            executable='velocity_subscriber',
            namespace='robot2',
            name='velocity_subscriber_node',
            output='screen'
        )
    ])
