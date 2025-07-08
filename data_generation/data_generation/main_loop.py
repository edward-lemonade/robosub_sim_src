import rclpy
from rclpy.node import Node

import random
import cv2
import numpy as np

from geometry_msgs.msg import Pose, Point, Quaternion
from robot_localization import SetPose
from ros_gz_interfaces.srv import SetEntityPose
from ros_gz_interfaces.msg import Entity
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from std_msgs.msg import Int32MultiArray

from datetime import datetime

class MainLoop(Node):
	def __init__(self):
		super().__init__('mainloop')

		self.model_name = 'high_level_robosub'  # Set your Gazebo model name
		self.image_sub = self.create_subscription(Image, '/robosub/camera/simulated_image', self.image_callback, 10)
		self.bridge = CvBridge()

		#self.pose_client = self.create_client(SetEntityPose, '/world/pool/set_entity_pose')
		self.pose_client = self.create_client(SetPose, '/world/pool/set_pose')
		while not self.pose_client.wait_for_service(timeout_sec=1.0):
			continue
		self.create_timer(0.5, self.move_model_entitypose)
		self.get_logger().info('Pose client ready')

	def move_model_entitypose(self):
		pose = Pose()
		pose.position = Point(x=random.uniform(-5, 5), y=random.uniform(-5, 5), z=random.uniform(0, 2))
		q = self.random_quaternion()
		pose.orientation = Quaternion(x=q[0], y=q[1], z=q[2], w=q[3])

		request = SetEntityPose.Request()
		request.entity = Entity(name='high_level_robosub')
		request.pose = pose

		self.pose_client.call_async(request)
		self.get_logger().info(f'Moved model to position {pose.position} and orientation {pose.orientation}')
		
	def move_model_pose(self):
		pose = Pose()
		pose.position = Point(x=random.uniform(-5, 5), y=random.uniform(-5, 5), z=random.uniform(0, 2))
		q = self.random_quaternion()
		pose.orientation = Quaternion(x=q[0], y=q[1], z=q[2], w=q[3])

		request = SetPose.Request()
		request.entity = Entity(name='high_level_robosub')
		request.pose = pose

		self.pose_client.call_async(request)
		self.get_logger().info(f'Moved model to position {pose.position} and orientation {pose.orientation}')

	def random_quaternion(self):
		u1, u2, u3 = random.random(), random.random(), random.random()
		qx = (1 - u1)**0.5 * np.sin(2 * np.pi * u2)
		qy = (1 - u1)**0.5 * np.cos(2 * np.pi * u2)
		qz = u1**0.5 * np.sin(2 * np.pi * u3)
		qw = u1**0.5 * np.cos(2 * np.pi * u3)
		return (qx, qy, qz, qw)

	def image_callback(self, msg):
		try:
			cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='rgb8')
			filename = f"images/image_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png"
			success = cv2.imwrite(filename, cv_image)
			self.get_logger().info(f"Saved image to {filename}: {success}")
		except Exception as e:
			self.get_logger().error(f"Failed to save image: {e}")
		
def main(args=None):	
	rclpy.init(args=None) # the rclpy library is initialized
	loop = MainLoop() # The node listenkey is created
	rclpy.spin(loop) # The node listenkey is spinned, meaning its callbacks are called
	
	loop.destroy_node() # Destroy the node explicitly
	rclpy.shutdown()

if __name__ == '__main__':
	main()