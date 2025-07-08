from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument, OpaqueFunction


def launch_setup(context, *args, **kwargs):
	robosub_bridge_arguments = (
		[
			"/robosub/camera/image@sensor_msgs/msg/Image@gz.msgs.Image",
			"/robosub/camera/simulated_image@sensor_msgs/msg/Image@gz.msgs.Image",
			"/robosub/camera/camera_info@sensor_msgs/msg/CameraInfo@gz.msgs.CameraInfo",
			"/world/pool/set_entity_pose@ros_gz_interfaces.srv.SetEntityPose_Request",
			"/world/pool/set_pose@robot_localization.srv.SetPose_Request",
		]
	)
	robosub_bridge = Node(
		package="ros_gz_bridge",
		executable="parameter_bridge",
		arguments=robosub_bridge_arguments,
		output="screen",
	)

	movement = Node(
		package="robosub_wrench_movement",
		executable="wrench_movement",
		output="screen",
	)

	keyInput = Node(
		package="controls_6dof",
		executable="listenkey",
		output="screen",
	)

	dataGen = Node(
		package="data_generation",
		executable="mainloop",
		output="screen",
	)

	return [dataGen]
	#return [robosub_bridge, movement, keyInput]


def generate_launch_description():
	args = [
		DeclareLaunchArgument(
			"namespace",
			default_value="",
			description="Namespace",
		),
	]

	return LaunchDescription(args + [OpaqueFunction(function=launch_setup)])
