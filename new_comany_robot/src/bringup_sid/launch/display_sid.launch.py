from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    # Declare the package name and xacro file name as arguments
    declare_package_name_arg = DeclareLaunchArgument(
        'package_name',
        default_value='sid_discription',
        description='Name of the ROS 2 package containing the xacro file'
    )


    declare_xacro_file_name_arg = DeclareLaunchArgument(
        'xacro_file_name',
        default_value='sid.urdf.xacro',
        description='Name of the XACRO file (e.g., robot.xacro)'
    )

    # Get the launch arguments
    package_name = LaunchConfiguration('package_name')
    xacro_file_name = LaunchConfiguration('xacro_file_name')

    # Find package share directory
    pkg_share = FindPackageShare(package=package_name)

    # Path to the xacro file
    xacro_file_path = PathJoinSubstitution([pkg_share, 'urdf', xacro_file_name])

    # Path to the rviz config file (optional)
    rviz_config_path = PathJoinSubstitution([pkg_share, 'config', 'sid_rviz.rviz'])

    # Use xacro to process the file and generate robot description
    robot_description_content = Command(
        [
            FindExecutable(name='xacro'), ' ', xacro_file_path
        ]
    )

    # Robot state publisher node
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_content}]
    )

    # Joint state publisher GUI (for interactive joint control)
    joint_state_publisher_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        output='screen'
    )

    # RViz2 node
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
        arguments=['-d', rviz_config_path]
    )

    return LaunchDescription([
        declare_package_name_arg,
        declare_xacro_file_name_arg,
        robot_state_publisher_node,
        joint_state_publisher_gui_node,
        rviz_node
    ])