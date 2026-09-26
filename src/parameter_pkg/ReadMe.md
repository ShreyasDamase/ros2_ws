## 1. run this command to use parameter_node

```bash

ros2 run parameter_pkg parameter --ros-args -p robot_speed:=2.7 
```

will give following output
[INFO] [1790350156.239351000] [parameter_node]: Parameter robot_speed:2.7

## 2.get parameter list by following commad

```bash
ros2 param list
```

will show:
ros2_ws % ros2 param list /parameter_node:
robot_speed start_type_description_service use_sim_time

```bash
ros2 param describe /parameter_node robot_speed
```

## 3. this will give description about parameter:

Parameter name: robot_speed Type: double Constraints:

## 4. this will give current parameter value with data type

```bash
ros2 param get /parameter_node robot_speed
```

Double value is: 2.7

## 5.Set runtime parameter with callback parameter way

run command:

```bash 
ros2 param set /parameter_callback_node robot_speed 3.5
```

outputed:

```bash
expected Set parameter successful
```

and

```bash
[INFO] [1790353047.576396000] [parameter_callback_node]: parameter for parameter_callback_node changed as robot_speed: 3.5 
```