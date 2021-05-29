# perception_genie

This node will subscribe '/ground_truth' topic which publish absolute obejct information in world.

Please run below command to make a relative information around target centered object.

If target object name is 'cloi1' and tracking id is '1', give an arguments as ros-args like below.

```shell
ros2 run perception_genie ground_truth --ros-args -r __ns:=/cloi1 -p tracking_id:=1
```

Then it will publish the data on  '/cloi1/ground_truth' topic.

The publishing data is very simple.

```python
target_object.position - other_object.position
target_object.velocity - other_object.velocity
```

That's it.