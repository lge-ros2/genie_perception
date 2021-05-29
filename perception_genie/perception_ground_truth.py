
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter

from std_msgs.msg import Header
from perception_msgs.msg import ObjectArray, ObjectInfo
from geometry_msgs.msg import Vector3, Polygon

class PerceptionGroundTruth(Node):

    def __init__(self):
        super().__init__('perception_ground_truth')

        self.declare_parameter('tracking_id', -1)
        self.tracking_id_ = self.get_parameter('tracking_id').value

        self.namespace_ = self.get_namespace() if not self.get_namespace().__eq__("/") else "need_to_add_namespace"

        self.get_logger().info("namespace: %s, target tracking_id: %d" % (self.get_namespace(), self.tracking_id_))

        self.subscription = self.create_subscription(
            ObjectArray,
            '/ground_truth',
            self.listener_callback,
            5)

        self.publisher = self.create_publisher(
            ObjectArray,
            self.namespace_ + '/ground_truth',
            10
            )


    def listener_callback(self, msg):

        pub_msg = ObjectArray()
        pub_msg.header = msg.header

        # msg_header_time = msg.header.stamp
        # self.get_logger().info('Header Time: %d.%d' % (msg_header_time.sec, msg_header_time.nanosec))

        # find target tracking id
        # output = [idx for idx, element in enumerate(msg.objects) if element.tracking_id == self.tracking_id_]
        # res = [x for i, item in enumerate(msg.objects) if x.tracking_id == self.tracking_id_]

        # output = (element.tracking_id == self.tracking_id_ for element in msg.objects)

        filtered_target_object = list(filter(lambda x: x.tracking_id == self.tracking_id_, msg.objects));
        target_object = None if len(filtered_target_object) == 0 else filtered_target_object[0]
        # self.get_logger().info('result = %d' % (target_object.tracking_id))

        if target_object is not None :

            for objectinfo in msg.objects:

                if objectinfo.tracking_id != self.tracking_id_ :
                    # objectinfo_header_time = objectinfo.header.stamp;
                    # self.get_logger().info('====================================')
                    # self.get_logger().info('object header Time: %d.%d' % (objectinfo_header_time.sec, objectinfo_header_time.nanosec))
                    # self.get_logger().info('tracking id: %d' % objectinfo.tracking_id)
                    # self.get_logger().info('class id: %d' % objectinfo.class_id)
                    # self.get_logger().info('position: "x:%f" y:%f z:%f"' % (objectinfo.position.x, objectinfo.position.y, objectinfo.position.z))
                    # self.get_logger().info('velocity: "x:%f" y:%f z:%f"' % (objectinfo.velocity.x, objectinfo.velocity.y, objectinfo.velocity.z))
                    # self.get_logger().info('size: "x:%f y:%f" z:%f"' % (objectinfo.size.x, objectinfo.size.y, objectinfo.size.z))
                    # self.get_logger().info('footprint: %d' % len(objectinfo.footprint.points))
                    new_object_relative_info = objectinfo

                    new_object_relative_info.position.x = target_object.position.x - new_object_relative_info.position.x
                    new_object_relative_info.position.y = target_object.position.y - new_object_relative_info.position.y
                    new_object_relative_info.position.z = target_object.position.z - new_object_relative_info.position.z

                    new_object_relative_info.velocity.x = target_object.velocity.x - new_object_relative_info.velocity.x
                    new_object_relative_info.velocity.y = target_object.velocity.y - new_object_relative_info.velocity.y
                    new_object_relative_info.velocity.z = target_object.velocity.z - new_object_relative_info.velocity.z

                    pub_msg.objects.append(new_object_relative_info)


        if len(pub_msg.objects) > 0:
            self.publisher.publish(pub_msg)


def main(args=None):
    print('Hi, this is perception_genie!!!')
    rclpy.init(args=args)
    perception_ground_truth_node = PerceptionGroundTruth()
    rclpy.spin(perception_ground_truth_node)
    perception_ground_truth_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
