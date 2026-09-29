from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    turtle_sim_node = Node(
        package='turtlesim',
        executable='turtlesim_node',
        name='turtlesim'
    )
    velocity_publisher_node = Node(
        package='turtle_runtime_demo',
        executable='turtle_runtime_demo',
        name='turtle_runtime_demo'
    )

    return LaunchDescription([
        turtle_sim_node,
        velocity_publisher_node
    ])
