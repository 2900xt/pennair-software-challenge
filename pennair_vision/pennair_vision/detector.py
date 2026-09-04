import json

import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String

from pennair_vision.main import annotate, centroid, detect, image_to_world, z_o


class Detector(Node):
    """Runs the shape-detection algorithm on each incoming frame and
    publishes the detections plus an annotated preview image."""

    def __init__(self):
        super().__init__('detector')
        self.bridge = CvBridge()
        self.create_subscription(Image, 'image_raw', self.on_image, 10)
        self.detections_pub = self.create_publisher(String, 'detections', 10)
        self.annotated_pub = self.create_publisher(Image, 'image_annotated', 10)
        self.get_logger().info('detector ready')

    def on_image(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        contours = detect(frame)

        detections = []
        for contour in contours:
            point = centroid(contour)
            if point is None:
                continue
            x_o, y_o = image_to_world(*point)
            detections.append({
                'center': [x_o, y_o, z_o],
                'outline': contour.reshape(-1, 2).tolist(),
            })

        self.detections_pub.publish(String(data=json.dumps(detections)))
        self.annotated_pub.publish(
            self.bridge.cv2_to_imgmsg(annotate(frame, contours), encoding='bgr8'))


def main(args=None):
    rclpy.init(args=args)
    node = Detector()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
