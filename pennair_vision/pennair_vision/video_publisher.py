import cv2
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image


class VideoPublisher(Node):
    """Streams a video file frame-by-frame onto the 'image_raw' topic."""

    def __init__(self):
        super().__init__('video_publisher')
        self.declare_parameter('video_path', 'PennAir 2024 App Dynamic.mp4')
        self.declare_parameter('fps', 30.0)

        video_path = self.get_parameter('video_path').value
        fps = self.get_parameter('fps').value

        self.cap = cv2.VideoCapture(video_path)
        if not self.cap.isOpened():
            self.get_logger().error(f'could not open video: {video_path}')
            raise SystemExit(1)

        self.bridge = CvBridge()
        self.publisher_ = self.create_publisher(Image, 'image_raw', 10)
        self.create_timer(1.0 / fps, self.tick)
        self.get_logger().info(f'streaming {video_path}')

    def tick(self):
        # One frame in, one frame out -- never load the whole video at once.
        ok, frame = self.cap.read()
        if not ok:
            # Loop back to the start so the demo keeps running.
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ok, frame = self.cap.read()
            if not ok:
                return
        self.publisher_.publish(self.bridge.cv2_to_imgmsg(frame, encoding='bgr8'))


def main(args=None):
    rclpy.init(args=args)
    node = VideoPublisher()
    try:
        rclpy.spin(node)
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
