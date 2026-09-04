import cv2, rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class Viewer(Node):
    def __init__(self):
        super().__init__('viewer')
        self.bridge = CvBridge()
        self.create_subscription(Image, 'image_annotated', self.show, 10)
    def show(self, msg):
        cv2.imshow('pennair', self.bridge.imgmsg_to_cv2(msg, 'bgr8'))
        cv2.waitKey(1)

rclpy.init(); rclpy.spin(Viewer())