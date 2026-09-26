# ROS 2 Python Launch File

## 1. Create the launch file

Create a Python launch file, for example:

```text
launch/launch.py
```

The launch file should import:

```python
from launch import LaunchDescription
from launch_ros.actions import Node
```

Then create the required function:

```python
def generate_launch_description():
```

The function name **must be exactly** `generate_launch_description`.

It cannot be changed to something like:

```python
def XYZ():
```

because `ros2 launch` looks for `generate_launch_description()`.

---

## 2. Create the LaunchDescription

Inside `generate_launch_description()`, return a `LaunchDescription` containing the nodes that should be started:

```python
def generate_launch_description():
    return LaunchDescription([
        Node(
            package='parameter_pkg',
            executable='parameter',
            name='parameter_node',
            output='screen'
        ),

        Node(
            package='parameter_pkg',
            executable='parameter_callback',
            name='parameter_callback_node',
            output='screen'
        )
    ])
```

### Node parameters

Each `Node` contains:

```python
Node(
    package='parameter_pkg',
    executable='parameter',
    name='parameter_node',
    output='screen'
)
```

- `package` → the ROS 2 package containing the executable.
- `executable` → the executable name defined in `setup.py`.
- `name` → the name given to the running ROS 2 node.
- `output='screen'` → output/logs are shown in the terminal.

---

## 3. Update `setup.py`

The launch file must be installed with the package.

Add this to `data_files`:

```python
('share/' + package_name + '/launch',
 ['launch/launch.py']),
```

For example:

```python
data_files = [
    ('share/ament_index/resource_index/packages',
     ['resource/' + package_name]),

    ('share/' + package_name,
     ['package.xml']),

    ('share/' + package_name + '/launch',
     ['launch/launch.py']),
],
```

The important part is:

```python
('share/' + package_name + '/launch',
 ['launch/launch.py']),
```

---

## 4. Build the workspace

From the ROS 2 workspace:

```bash
colcon build
```

---

## 5. Source the workspace

After building:

```bash
source install/setup.bash
```

For zsh:

```bash
source install/setup.zsh
```

---

## 6. Run the launch file

Use:

```bash
ros2 launch <package_name> <launch_file_name>
```

For this example:

```bash
ros2 launch launch_pkg launch.py
```

The launch system will find:

```python
generate_launch_description()
```

and execute the nodes defined inside the `LaunchDescription`.

---

## Complete flow

```text
Create launch.py
       ↓
Import LaunchDescription and Node
       ↓
Create generate_launch_description()
       ↓
Add Node objects
       ↓
Update setup.py data_files
       ↓
colcon build
       ↓
source install/setup.bash
       ↓
ros2 launch launch_pkg launch.py
```

---
---
---

# ROS 2 Launch Arguments

A launch argument allows a value to be supplied from the command line when starting a launch file.

## 1. Import `DeclareLaunchArgument`

Add:

```python
from launch.actions import DeclareLaunchArgument
```

`DeclareLaunchArgument` is used to **declare a launch-time argument**.

Example:

```python
robot_speed_arg = DeclareLaunchArgument(
    'robot_speed',
    default_value='2.0',
    description='Initial robot speed'
)
```

Here:

- `robot_speed` → name of the launch argument.
- `default_value='2.0'` → value used when no value is provided from the command line.
- `description` → description of the argument.

---

## 2. Import `LaunchConfiguration`

Add:

```python
from launch.substitutions import LaunchConfiguration
```

`LaunchConfiguration` is used to **access the value of a launch argument**.

Example:

```python
robot_speed = LaunchConfiguration('robot_speed')
```

This means:

> Get the current value of the launch argument named `robot_speed`.

It is a launch substitution, not a ROS parameter.

---

## 3. Add the declared argument to `LaunchDescription`

The declared launch argument must be included in the returned `LaunchDescription`:

```python
return LaunchDescription([
    robot_speed_arg,

    Node(
        package='parameter_pkg',
        executable='parameter',
        name='parameter_node',
        parameters=[{'robot_speed': robot_speed}],
        output='screen'
    )
])
```

The purpose of:

```python
robot_speed_arg,
```

is to register the launch argument with the launch system.

---

## 4. Pass the launch argument value to a ROS parameter

The launch argument value can then be passed to a ROS node parameter:

```python
parameters = [{'robot_speed': robot_speed}]
```

Here:

```text
launch argument
robot_speed
     ↓
LaunchConfiguration('robot_speed')
     ↓
ROS node parameter
robot_speed
```

The launch argument and ROS parameter happen to have the same name here, but they are two different concepts.

---

## 5. Add the new launch file to `setup.py`

When creating another launch file, add that file to `data_files` in `setup.py`.

For example:

```python
data_files = [
    ('share/ament_index/resource_index/packages',
     ['resource/' + package_name]),

    ('share/' + package_name,
     ['package.xml']),

    ('share/' + package_name + '/launch',
     ['launch/launch.py']),

    ('share/' + package_name + '/launch',
     ['launch/launch_argument.py']),
],
```

The new launch file must therefore be installed with the package.

---

## 6. Build and source

After changing `setup.py`:

```bash
colcon build
```

Then:

```bash
source install/setup.bash
```

For zsh:

```bash
source install/setup.zsh
```

---

## 7. Pass the launch argument from the command line

Run:

```bash
ros2 launch launch_pkg launch_argument.py robot_speed:=3.0
```

This passes:

```text
robot_speed = 3.0
```

to the launch argument.

The launch system then resolves:

```python
LaunchConfiguration('robot_speed')
```

to:

```text
3.0
```

and passes that value to the ROS parameter:

```python
parameters = [{'robot_speed': robot_speed}]
```

---

## 8. `:=` syntax

The launch argument must be written as one command-line argument:

```bash
robot_speed:=3.0
```

There should be **no spaces** around `:=`.

Correct:

```bash
robot_speed:=3.0
```

Incorrect:

```bash
robot_speed := 3.0
```

The reason is that the shell separates space-separated text into different command-line arguments, so `robot_speed:=3.0`
must remain a single argument.

---

## Complete flow

```text
DeclareLaunchArgument
        ↓
robot_speed
        ↓
LaunchConfiguration('robot_speed')
        ↓
LaunchDescription
        ↓
Node parameters
        ↓
ROS parameter: robot_speed
        ↓
Command line:
robot_speed:=3.0
```

## Complete launch file

```python
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    robot_speed_arg = DeclareLaunchArgument(
        'robot_speed',
        default_value='2.0',
        description='Initial robot speed'
    )

    robot_speed = LaunchConfiguration('robot_speed')

    return LaunchDescription([
        robot_speed_arg,

        Node(
            package='parameter_pkg',
            executable='parameter',
            name='parameter_node',
            parameters=[{'robot_speed': robot_speed}],
            output='screen'
        ),

        Node(
            package='parameter_pkg',
            executable='parameter_callback',
            name='parameter_callback_node',
            output='screen'
        )
    ])
```

### The key distinction

```text
DeclareLaunchArgument
→ declares a launch argument

LaunchConfiguration
→ gets the launch argument's value

parameters=[...]
→ passes that value to a ROS parameter
```

So your command:

```bash
ros2 launch launch_pkg launch_argument.py robot_speed:=3.0
```

ultimately results in the ROS node receiving:

```text
robot_speed = 3.0
```


