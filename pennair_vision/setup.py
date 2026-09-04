from glob import glob

from setuptools import find_packages, setup

package_name = 'pennair_vision'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    description='idk what to put here',
    entry_points={
        'console_scripts': [
            'video_publisher = pennair_vision.video_publisher:main',
            'detector = pennair_vision.detector:main',
            'viewer = pennair_vision.viewer:main',
        ],
    },
)
