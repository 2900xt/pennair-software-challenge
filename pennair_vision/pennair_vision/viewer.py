import cv2
import rclpy
from cv_bridge import CvBridge
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from sensor_msgs.msg import Image


class Viewer(Node):
    """Displays the 'image_annotated' topic in a cv2 window."""

    def __init__(self):
        super().__init__('viewer')
        self.bridge = CvBridge()
        self.create_subscription(Image, 'image_annotated', self.show, 10)
        cv2.namedWindow('pennair', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('pennair', 640, 360)

    def show(self, msg):
        cv2.imshow('pennair', self.bridge.imgmsg_to_cv2(msg, 'bgr8'))
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    node = Viewer()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
