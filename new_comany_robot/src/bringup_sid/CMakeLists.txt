cmake_minimum_required(VERSION 3.8)
project(bringup_sid)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY config launch world 
  DESTINATION share/bringup_sid/
)

ament_package()
