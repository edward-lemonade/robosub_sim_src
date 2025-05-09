cmake_minimum_required(VERSION 3.8)
project(dave_gz_sensor_plugins)

# Find required packages
find_package(ament_cmake REQUIRED)
find_package(gz-cmake3 REQUIRED)
find_package(gz-plugin2 REQUIRED COMPONENTS register)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(gz-common5 REQUIRED COMPONENTS profiler)
find_package(gz-sim8 REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(dave_interfaces REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(Protobuf REQUIRED)
find_package(gz-msgs10 REQUIRED)
find_package(OpenCV REQUIRED)

# Set version variables
set(GZ_PLUGIN_VER ${gz-plugin2_VERSION_MAJOR})
set(GZ_COMMON_VER ${gz-common5_VERSION_MAJOR})
set(GZ_SIM_VER ${gz-sim8_VERSION_MAJOR})
set(GZ_MSGS_VER ${gz-msgs10_VERSION_MAJOR})

include_directories(${OpenCV_INCLUDE_DIRS})

message(STATUS "Compiling against Gazebo Harmonic")

add_library(UsblTransceiver SHARED src/UsblTransceiver.cc)
add_library(UsblTransponder SHARED src/UsblTransponder.cc)
add_library(sea_pressure_sensor SHARED src/sea_pressure_sensor.cc)
add_library(UnderwaterCamera SHARED src/UnderwaterCamera.cc)

target_include_directories(UsblTransceiver PRIVATE include)
target_include_directories(UsblTransponder PRIVATE include)
target_include_directories(sea_pressure_sensor PRIVATE include)
target_include_directories(UnderwaterCamera PRIVATE include)

target_link_libraries(UsblTransceiver
  gz-sim${GZ_SIM_VER}::gz-sim${GZ_SIM_VER}
)

target_link_libraries(UsblTransponder
  gz-sim${GZ_SIM_VER}::gz-sim${GZ_SIM_VER}
)

target_link_libraries(sea_pressure_sensor
  gz-sim${GZ_SIM_VER}::gz-sim${GZ_SIM_VER}
)

target_link_libraries(UnderwaterCamera
  gz-sim${GZ_SIM_VER}::gz-sim${GZ_SIM_VER}
  ${OpenCV_LIBS}
)

# Specify dependencies for FullSystem using ament_target_dependencies
ament_target_dependencies(UsblTransceiver
  dave_interfaces
  sensor_msgs
  rclcpp
  geometry_msgs
  std_msgs
)

ament_target_dependencies(UsblTransponder
  dave_interfaces
  rclcpp
  std_msgs
)

ament_target_dependencies(sea_pressure_sensor
  rclcpp
  std_msgs
  sensor_msgs
  geometry_msgs
)

ament_target_dependencies(UnderwaterCamera
  rclcpp
  sensor_msgs
)

# Install targets
install(
  TARGETS
    UsblTransceiver
    UsblTransponder
    sea_pressure_sensor
    UnderwaterCamera
  DESTINATION lib/${PROJECT_NAME}
)

# Install headers
install(DIRECTORY include/
  DESTINATION include/
)

# Environment hooks
ament_environment_hooks(
  "${CMAKE_CURRENT_SOURCE_DIR}/hooks/${PROJECT_NAME}.dsv.in"
)

# Testing setup
if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
