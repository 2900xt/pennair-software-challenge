from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    video_path_arg = DeclareLaunchArgument(
        'video_path',
        default_value='PennAir 2024 App Dynamic.mp4',
        description='Path to the video file to stream',
    )

    return LaunchDescription([
        video_path_arg,
        Node(
            package='pennair_vision',
            executable='video_publisher',
            parameters=[{'video_path': LaunchConfiguration('video_path')}],
        ),
        Node(
            package='pennair_vision',
            executable='detector',
        ),
    ])
