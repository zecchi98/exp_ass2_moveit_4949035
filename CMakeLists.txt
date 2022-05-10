cmake_minimum_required(VERSION 3.1.3)
project(exp_ass2_moveit_4949035)

find_package(catkin REQUIRED COMPONENTS
  roscpp
  rospy
  std_msgs
  visualization_msgs
  gazebo_msgs
  message_generation
  rosplan_planning_system
)
 add_message_files(
   FILES
   ErlOracle.msg
#   Message2.msg
 )
 
 add_service_files(
   FILES
   Oracle.srv
   comunication.srv
#   Service2.srv
 )
 
  generate_messages(
   DEPENDENCIES
   std_msgs
 )
 
catkin_package()


include_directories(
include
  ${catkin_INCLUDE_DIRS}
)
 add_executable(simulation_node src/simulation_node.cpp)

 add_executable(myaction src/my_action.cpp)

 add_dependencies(myaction ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

 target_link_libraries(simulation_node
   ${catkin_LIBRARIES}
 )
 target_link_libraries(myaction
   ${catkin_LIBRARIES}
 )

catkin_install_python(PROGRAMS scripts/robot_control.py scripts/ID_handler.py scripts/state_machine.py
DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
)

install(DIRECTORY launch DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
  PATTERN "setup_assistant.launch" EXCLUDE)
install(DIRECTORY config DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION})
