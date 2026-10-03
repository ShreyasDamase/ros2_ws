# ROS 2 Service and Action Example — SetRobotSpeed

This README documents a small ROS 2 Python example used to learn the difference between a service and an action, and to build a working action server and action client.

The example uses a `SetRobotSpeed`-style interface with:

- Goal/request: `target_speed`, `gradual`
- Result/response: `success`, `applied_speed`, `message`
- Action feedback: `current_speed`, `progress`

The examples use the package `robot_interface` for the custom interfaces and a Python package such as `robot_speed_service` for the server/client nodes.

---

## 1. Service vs Action

### Service

A service is a request/response interaction:

```text
Client
  |
  | request
  v
Server
  |
  | response
  v
Client
```

Example service interface:

```text
float32 target_speed
bool gradual
---
bool success
float32 applied_speed
string message
```

Use a service when the operation is normally short and there is no need for continuous progress feedback.

### Action

An action has three parts:

```text
Goal
---
Result
---
Feedback
```

Conceptually:

```text
Client
  |
  | goal
  v
Action Server
  |
  |---- feedback ----> Client
  |
  |---- feedback ----> Client
  |
  |---- result -------> Client
```

Actions are useful for longer-running operations where feedback, cancellation, or a final result are important.

---

## 2. Action Interface Used in This Example

The action definition is stored in the interface package under:

```text
robot_interface/
└── action/
    └── SetRobotSpeedAction.action
```

The interface is:

```text
float32 target_speed
bool gradual
---
bool success
float32 applied_speed
string message
---
float32 current_speed
float32 progress
```

The three sections mean:

```text
GOAL
float32 target_speed
bool gradual

RESULT
bool success
float32 applied_speed
string message

FEEDBACK
float32 current_speed
float32 progress
```

### Important directory rule

The `.action` file belongs in the package's `action/` directory.

Correct:

```text
robot_interface/
├── action/
│   └── SetRobotSpeedAction.action
├── robot_interface/
│   └── ... Python package files ...
├── package.xml
└── setup.py
```

Do not put the `.action` definition inside the Python server/client source directory.

This was the first mistake in this exercise: the action file was initially placed in the wrong location instead of the package-level `action/` directory.

---

## 3. Create the Interface Package

Create the package from the workspace `src` directory:

```bash
cd ~/ros2_ws/src

ros2 pkg create robot_interface \
  --build-type ament_cmake
```

Create the action directory:

```bash
cd robot_interface
mkdir action
```

Create the action file:

```bash
touch action/SetRobotSpeedAction.action
```

Edit the file and add the three-section action definition shown above.

---

## 4. Register the Action Interface for Generation

The interface package must use ROS 2 interface generation.

In `package.xml`, the package needs the interface-generation dependencies and interface-package membership, including the equivalents of:

```xml
<buildtool_depend>rosidl_default_generators</buildtool_depend>
<exec_depend>rosidl_default_runtime</exec_depend>
<member_of_group>rosidl_interface_packages</member_of_group>
```

In `CMakeLists.txt`, register the action with `rosidl_generate_interfaces(...)` and include the action file, for example:

```cmake
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "action/SetRobotSpeedAction.action"
)
```

The exact dependency list may also include the standard interface packages required by the interface definition.

### Why this is required

Writing a `.action` file is not enough. ROS 2 must generate language-specific code from it.

After generation, Python code can import the generated action type:

```python
from robot_interface.action import SetRobotSpeedAction
```

---

## 5. Where the Generated Interface Goes

The source definition remains in:

```text
robot_interface/action/SetRobotSpeedAction.action
```

After building, ROS 2 generates/install artifacts under the workspace `build/`, `install/`, and related generated locations.

You normally do not edit those generated files manually.

The application code uses the generated Python interface through:

```python
from robot_interface.action import SetRobotSpeedAction
```

The custom interface type can be verified with:

```bash
ros2 interface show robot_interface/action/SetRobotSpeedAction
```

---

## 6. Build the Interface Package

From the workspace root:

```bash
cd ~/ros2_ws
colcon build --packages-select robot_interface
```

Then source the workspace:

```bash
source install/setup.zsh
```

If you use the Pixi ROS 2 environment from this setup:

```bash
pixi shell --manifest-path ~/ros2_lyrical/pixi.toml
source install/setup.zsh
```

Verify the generated interface:

```bash
ros2 interface show robot_interface/action/SetRobotSpeedAction
```

---

## 7. Create the Python Node Package

The server and client are regular Python ROS 2 nodes. In this exercise they are placed in a package such as:

```text
robot_speed_service
```

Create it with:

```bash
cd ~/ros2_ws/src

ros2 pkg create robot_speed_service \
  --build-type ament_python \
  --dependencies rclpy
```

The package can then contain Python modules such as:

```text
robot_speed_service/
├── robot_speed_service/
│   ├── __init__.py
│   ├── speed_server.py
│   ├── speed_client.py
│   ├── speed_action_server.py
│   └── speed_action_client.py
├── resource/
│   └── robot_speed_service
├── package.xml
└── setup.py
```

The important architecture is:

```text
robot_interface
    -> custom service/action definitions

robot_speed_service
    -> executable server/client nodes using those definitions
```

Keeping interfaces separate from application nodes is a useful ROS 2 package structure.

---

## 8. Dependencies for the Python Action Client/Server

For the Python nodes in this example, the main dependencies are:

```text
rclpy
```

and the custom interface package:

```text
robot_interface
```

For the action server:

```python
from rclpy.action import ActionServer
from robot_interface.action import SetRobotSpeedAction
```

For the action client:

```python
from rclpy.action import ActionClient
from robot_interface.action import SetRobotSpeedAction
```

The package containing the nodes must declare the required dependencies in `package.xml`.

---

## 9. Register Server and Client in setup.py

`setup.py` exposes Python functions as ROS 2 executables through `console_scripts`.

The relevant pattern is:

```python
entry_points={
    'console_scripts': [
        'speed_server = robot_speed_service.speed_server:main',
        'speed_client = robot_speed_service.speed_client:main',
        'speed_action_server = robot_speed_service.speed_action_server:main',
        'speed_action_client = robot_speed_service.speed_action_client:main',
    ],
},
```

The pattern is:

```text
'executable_name = python_package.python_module:main_function'
```

After changing `setup.py`, rebuild the package:

```bash
cd ~/ros2_ws
colcon build --packages-select robot_speed_service
source install/setup.zsh
```

Then run nodes with:

```bash
ros2 run robot_speed_service speed_action_server
ros2 run robot_speed_service speed_action_client
```

---

## 10. Action Server Pattern

The action server is created with:

```python
self.action_server_ = ActionServer(
    self,
    SetRobotSpeedAction,
    'set_robot_speed',
    self.execute_callback
)
```

The important arguments are:

```text
1. Node
2. Action type
3. Action name
4. Execute callback
```

The action name becomes:

```text
/set_robot_speed
```

### execute_callback pattern

Inside the callback, the useful pattern is:

```python
request = goal_handle.request
feedback = SetRobotSpeedAction.Feedback()
result = SetRobotSpeedAction.Result()
```

Here:

- `goal_handle.request` is the goal that the client sent.
- `Feedback()` creates the feedback message that the server publishes during execution.
- `Result()` creates the final result returned when execution is complete.

Then read the goal fields from `request`:

```python
target_speed = request.target_speed
gradual = request.gradual
```

Publish progress with:

```python
feedback.current_speed = ...
feedback.progress = ...
goal_handle.publish_feedback(feedback)
```

Finish successfully with:

```python
goal_handle.succeed()
return result
```

For cancellation handling, check:

```python
goal_handle.is_cancel_requested
```

and mark the goal as canceled with:

```python
goal_handle.canceled()
```

---

## 11. Action Client Pattern

The action client is created with:

```python
self.action_client_ = ActionClient(
    self,
    SetRobotSpeedAction,
    'set_robot_speed'
)
```

### Step 1: Wait for the action server

```python
while not self.action_client_.wait_for_server(timeout_sec=1.0):
    self.get_logger().info('Waiting for action server...')
```

This is the action equivalent of waiting for a service.

### Step 2: Create the goal

```python
goal = SetRobotSpeedAction.Goal()
goal.target_speed = target_speed
goal.gradual = gradual
```

### Step 3: Send the goal asynchronously

```python
future = self.action_client_.send_goal_async(
    goal,
    feedback_callback=self.feedback_callback
)
```

Register a callback for the goal response:

```python
future.add_done_callback(self.goal_response_callback)
```

### Step 4: Handle acceptance/rejection

The goal-response callback receives a future and extracts:

```python
goal_handle = future.result()
```

Then check:

```python
if not goal_handle.accepted:
    ...
```

If accepted, request the final result asynchronously:

```python
result_future = goal_handle.get_result_async()
result_future.add_done_callback(self.result_callback)
```

### Step 5: Receive feedback

The callback registered in `send_goal_async(...)` receives feedback while the action is running:

```python
feedback = feedback_msg.feedback
```

Read the fields:

```python
feedback.current_speed
feedback.progress
```

### Step 6: Receive the final result

The result callback extracts:

```python
result = future.result().result
```

Then read:

```python
result.success
result.applied_speed
result.message
```

---

## 12. Service Client Pattern Used in the Same Exercise

The service client uses:

```python
self.client_ = self.create_client(
    SetRobotSpeed,
    'speed'
)
```

Wait for the service:

```python
while not self.client_.wait_for_service(timeout_sec=1.0):
    self.get_logger().info('Speed service not available')
```

Create the request:

```python
request = SetRobotSpeed.Request()
request.target_speed = target_speed
request.gradual = gradual
```

Send asynchronously:

```python
future = self.client_.call_async(request)
```

Then wait for completion in this simple client:

```python
rclpy.spin_until_future_complete(self, future)
```

Finally:

```python
return future.result()
```

This gives a useful comparison with the action client.

---

## 13. Future and Async Patterns to Remember

These patterns are worth memorizing because they appear repeatedly in ROS 2 Python code.

### Service

```text
wait_for_service()
    -> call_async(request)
    -> spin_until_future_complete()
    -> future.result()
```

In code:

```python
future = self.client_.call_async(request)
rclpy.spin_until_future_complete(self, future)
response = future.result()
```

### Action

```text
wait_for_server()
    -> send_goal_async()
    -> add_done_callback(goal_response_callback)
    -> get_result_async()
    -> add_done_callback(result_callback)
```

Feedback is received through the callback passed to `send_goal_async()`.

---

## 14. `add_done_callback()` — What It Means

A future represents an operation that is not complete yet.

Instead of blocking and waiting for it, you can register a callback:

```python
future.add_done_callback(self.some_callback)
```

The callback runs when that future finishes.

For the action client there are two important future stages:

```text
send_goal_async()
        |
        v
future
        |
        +--> add_done_callback(goal_response_callback)
                              |
                              v
                         goal accepted
                              |
                              v
                     get_result_async()
                              |
                              v
                         result future
                              |
                              +--> add_done_callback(result_callback)
```

The main idea:

```text
async operation -> Future -> callback when complete
```

---

## 15. CLI Commands for Checking the Action

### List actions

```bash
ros2 action list
```

Expected example:

```text
/set_robot_speed
```

### Show action type

```bash
ros2 action type /set_robot_speed
```

This should identify the custom action type, for example:

```text
robot_interface/action/SetRobotSpeedAction
```

### Show action interface

```bash
ros2 interface show robot_interface/action/SetRobotSpeedAction
```

### Show action server/client information

```bash
ros2 action info /set_robot_speed
```

### Send a goal from the CLI

```bash
ros2 action send_goal \
  /set_robot_speed \
  robot_interface/action/SetRobotSpeedAction \
  "{target_speed: 100.0, gradual: true}"
```

To request feedback from the CLI:

```bash
ros2 action send_goal \
  /set_robot_speed \
  robot_interface/action/SetRobotSpeedAction \
  "{target_speed: 100.0, gradual: true}" \
  --feedback
```

The exact action type shown by `ros2 action type` should always be used if you are unsure of the generated name.

---

## 16. Run Order for the Complete Example

A reliable procedural workflow is:

### Terminal 1 — enter the ROS 2 environment

```bash
pixi shell --manifest-path ~/ros2_lyrical/pixi.toml
```

### Terminal 1 — source the workspace

```bash
cd ~/ros2_ws
source install/setup.zsh
```

### Terminal 1 — start the action server

```bash
ros2 run robot_speed_service speed_action_server
```

### Terminal 2 — enter the same environment

```bash
pixi shell --manifest-path ~/ros2_lyrical/pixi.toml
cd ~/ros2_ws
source install/setup.zsh
```

### Terminal 2 — run the action client

```bash
ros2 run robot_speed_service speed_action_client
```

### Or test without the Python client

Use:

```bash
ros2 action send_goal /set_robot_speed \
  robot_interface/action/SetRobotSpeedAction \
  "{target_speed: 100.0, gradual: true}" \
  --feedback
```

---

## 17. Useful Verification Sequence

When an action does not work, check from the lowest level upward:

```bash
ros2 interface show robot_interface/action/SetRobotSpeedAction
```

Then:

```bash
ros2 action list
```

Then:

```bash
ros2 action type /set_robot_speed
```

Then:

```bash
ros2 action info /set_robot_speed
```

Then test the server directly:

```bash
ros2 action send_goal /set_robot_speed \
  robot_interface/action/SetRobotSpeedAction \
  "{target_speed: 100.0, gradual: true}" \
  --feedback
```

If the CLI works but the Python client does not, the issue is probably in the client node or its package registration rather than the action interface/server.

---

## 18. Common Mistakes From This Exercise

### Mistake 1 — Action file in the wrong directory

Wrong idea:

```text
robot_interface/robot_interface/...
```

or inside the Python server source directory.

Correct:

```text
robot_interface/action/SetRobotSpeedAction.action
```

Then register that path with the ROS 2 interface-generation system.

### Mistake 2 — Mixing service terminology with action terminology

Service:

```text
Request
Response
```

Action:

```text
Goal
Feedback
Result
```

For the action:

```python
request = goal_handle.request
feedback = SetRobotSpeedAction.Feedback()
result = SetRobotSpeedAction.Result()
```

Do not use service-style `Request()` and `Response()` objects for an action.

### Mistake 3 — Confusing the action server with a goal

This command:

```bash
ros2 action list
```

shows the action endpoint:

```text
/set_robot_speed
```

It does not list individual active goals.

---

## 19. Service vs Action Code Pattern

### Service client

```text
create_client()
    |
    v
wait_for_service()
    |
    v
Request()
    |
    v
call_async()
    |
    v
spin_until_future_complete()
    |
    v
future.result()
```

### Action server

```text
ActionServer()
    |
    v
execute_callback()
    |
    +--> goal_handle.request
    |
    +--> Feedback()
    |      |
    |      +--> publish_feedback()
    |
    +--> Result()
           |
           +--> succeed()
           |
           +--> return result
```

### Action client

```text
ActionClient()
    |
    v
wait_for_server()
    |
    v
Goal()
    |
    v
send_goal_async()
    |
    +--> feedback_callback()
    |
    +--> goal_response_callback()
             |
             v
       get_result_async()
             |
             v
       result_callback()
```

---

## 20. Memory Pattern

Keep these pairs in mind:

```text
SERVICE
wait_for_service()
call_async()
spin_until_future_complete()
future.result()
```

```text
ACTION SERVER
ActionServer()
execute_callback()
goal_handle.request
Feedback()
publish_feedback()
Result()
succeed()
canceled()
```

```text
ACTION CLIENT
ActionClient()
wait_for_server()
Goal()
send_goal_async()
add_done_callback()
feedback_callback()
get_result_async()
result_callback()
```

A compact mental model:

```text
Service = request -> response

Action = goal -> feedback -> result

Future = operation not finished yet

Async = start the operation without blocking for its completion

add_done_callback() = run this function when the future completes
```

---

## 21. Final Example Flow

The complete `SetRobotSpeed` action exercise can be summarized as:

```text
1. Create robot_interface package
2. Create action/ directory
3. Create SetRobotSpeedAction.action
4. Define Goal / Result / Feedback
5. Register the action with rosidl
6. Build robot_interface
7. Verify ros2 interface show
8. Create Python node package
9. Add rclpy + robot_interface dependencies
10. Register server/client in setup.py
11. Build and source workspace
12. Start action server
13. Start action client
14. Send goal
15. Receive feedback
16. Receive final result
17. Test the same server with ros2 action send_goal
```

This is the reusable ROS 2 action workflow to carry into larger robotics projects such as navigation, motor control, trajectory execution, and manipulation.
