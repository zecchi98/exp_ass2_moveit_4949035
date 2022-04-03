#!/usr/bin/env python
## @package exp_ass2_moveit_4949035
# \file state_machine.py
# \brief This node is used as a state machine. In particular it will control the pddl interface by planning and requesting what's needed.
# \author Federico Zecchi
# \version 0.1
# \date 30/03/22
#
# \details
#
# Client : <BR>
# [/rosplan_knowledge_base/clear][/rosplan_knowledge_base/update][/rosplan_problem_interface/problem_generation_server]
# [/rosplan_planner_interface/planning_server][/rosplan_parsing_interface/parse_plan][/rosplan_plan_dispatcher/cancel_dispatch]
# [/rosplan_plan_dispatcher/dispatch_plan]
#
import copy
import math
import sys
import time
from logging import setLoggerClass
from math import cos, pi, sin
from os import access
from re import X

import geometry_msgs.msg
import moveit_commander
import moveit_msgs.msg
import numpy as np
import rospy
from moveit_commander import *
from moveit_commander.conversions import pose_to_list
from moveit_commander.move_group import MoveGroupCommander
from moveit_commander.robot import RobotCommander
from std_msgs.msg import String
from tf.transformations import euler_from_quaternion, quaternion_from_euler
from exp_ass2_moveit_4949035.srv import *
from exp_ass2_moveit_4949035.msg import ErlOracle

from std_srvs.srv import Empty
from rosplan_knowledge_msgs.srv import *

from rosplan_dispatch_msgs.srv import DispatchService

class my_rosplan_class():
  ##
  #\class my_rosplan_class
  #\brief This class has been developed in order to interface with pddl. From this class the problem file can be modified,
  #it is possible to clear a plan or plan a new one
  def __init__(self):
    ##
    #\brief In this function some clients initialization will be executed and we will wait for service to come up.
    super(my_rosplan_class, self).__init__()

    #Here we wait for services to be active
    print("Waiting for services")
    rospy.wait_for_service("rosplan_knowledge_base/update")
    rospy.wait_for_service("rosplan_knowledge_base/clear")
    rospy.wait_for_service("rosplan_problem_interface/problem_generation_server")
    rospy.wait_for_service("rosplan_planner_interface/planning_server")
    rospy.wait_for_service("rosplan_parsing_interface/parse_plan")
    rospy.wait_for_service("rosplan_plan_dispatcher/cancel_dispatch")
    rospy.wait_for_service("rosplan_plan_dispatcher/dispatch_plan")
    print("All services ready")

    #Here we initilize clients
    self.clear_plan=rospy.ServiceProxy('/rosplan_knowledge_base/clear',Empty)
    self.update_the_plan=rospy.ServiceProxy('/rosplan_knowledge_base/update',KnowledgeUpdateService)
    self.generate_problem_client=rospy.ServiceProxy('/rosplan_problem_interface/problem_generation_server',Empty)
    self.planning_server_client=rospy.ServiceProxy('/rosplan_planner_interface/planning_server',Empty)
    self.parse_plan_client=rospy.ServiceProxy('/rosplan_parsing_interface/parse_plan',Empty)
    self.cancel_dispatch_client=rospy.ServiceProxy('/rosplan_plan_dispatcher/cancel_dispatch',Empty)
    self.dispatch_client=rospy.ServiceProxy('/rosplan_plan_dispatcher/dispatch_plan',DispatchService)
    self.debug=False
  def clear_plan(self):
    ##
    #\brief We call the client to clear a plan
    self.clear_plan()
  def add_GOAL_predicate_single_param(self,predicate_name,key,value,bool):
    ##
    #\brief We use this function to add as a goal one predicate of a single param.
    #predicate_name is the name of the predicate
    #key is the type of the param (for example waypoint)
    #value is the name of the param variable (for example wp1)
    #bool is used to set to True or False the goal
    
    #Here we initialize the message and we call the client
    req=KnowledgeUpdateServiceRequest()
    req.knowledge.is_negative=not(bool)
    req.update_type=1
    req.knowledge.knowledge_type=1
    req.knowledge.attribute_name=predicate_name
    x=diagnostic_msgs.msg.KeyValue()
    x.key=key
    x.value=value
    req.knowledge.values.append(x)
    result=self.update_the_plan(req)
    if self.debug==True:
      print(result)
  def add_GOAL_predicate_NO_param(self,predicate_name,bool):
    ##
    #\brief We use this function to add as a goal one predicate without param.
    #predicate_name is the name of the predicate
    #bool is used to set to True or False the goal
    
    #Here we initialize the message and we call the client
    req=KnowledgeUpdateServiceRequest()
    req.knowledge.is_negative=not(bool)
    req.update_type=1
    req.knowledge.knowledge_type=1
    req.knowledge.attribute_name=predicate_name
    result=self.update_the_plan(req)
    if self.debug==True:
      print(result)
  def add_INSTANCE(self,type,name):
    ##
    #\brief We use this function to add an instance of a variable. For example to declare that wp1 as a waypoint
    #type is the type of the param (for example waypoint)
    #name is the name of the param variable (for example wp1)
    
    #Here we initialize the message and we call the client
    req=KnowledgeUpdateServiceRequest()

    req.update_type=0
    req.knowledge.knowledge_type=0
    req.knowledge.instance_name=name
    req.knowledge.instance_type=type
    result=self.update_the_plan(req)
    if self.debug==True:
      print(result)
  def add_FACT_predicate_single_param(self,predicate_name,key,value,bool):
    ##
    #\brief We use this function to initialize a predicate with a value. In this case it is a single param predicate
    #predicate_name is the name of the predicate
    #key is the type of the param (for example waypoint)
    #value is the name of the param variable (for example wp1)
    #bool is used to set to True or False the goal
    
    #Here we initialize the message and we call the client
    req=KnowledgeUpdateServiceRequest()
    req.knowledge.is_negative=not(bool)
    req.update_type=0
    req.knowledge.knowledge_type=1
    req.knowledge.attribute_name=predicate_name
    x=diagnostic_msgs.msg.KeyValue()
    x.key=key
    x.value=value
    req.knowledge.values.append(x)
    result=self.update_the_plan(req)
    if self.debug==True:
      print(result)
  def add_FACT_predicate_NO_param(self,predicate_name,bool):
    ##
    #\brief We use this function to initialize a predicate with a value. In this case it is a no param predicate
    #predicate_name is the name of the predicate
    #bool is used to set to True or False the goal
    
    #Here we initialize the message and we call the client
    req=KnowledgeUpdateServiceRequest()
    req.knowledge.is_negative=not(bool)
    req.update_type=0
    req.knowledge.knowledge_type=1
    req.knowledge.attribute_name=predicate_name
    result=self.update_the_plan(req)
    if self.debug==True:
      print(result)
  def generate_the_problem_and_plan_and_parse(self):
    ##
    #\brief This function is used to call the right clients to generate problem, plan and parse the plan
    self.generate_problem_client()
    self.planning_server_client()
    self.parse_plan_client()
  def cancel_dispatch(self):
    ##
    #\brief This function will call the right client to cancel a plan
    self.cancel_dispatch_client()
  def dispatch_plan(self):
    ##
    #\brief This function will dispatch a plan
    return self.dispatch_client()
def plan_a_test():
    ##
    #\brief We will enter in this function if and only if there is a new id to be checked.
    #We will ask through pddl to go to the center of the map and check if we have won.

    #We will check our position
    robot_at = rospy.get_param('/robot_at')
    robot_at="wp"+str(robot_at)

    #Clear the old plan
    rosplan_library.clear_plan()

    #Adding waypoint instances
    rosplan_library.add_INSTANCE("waypoint","wp0")
    rosplan_library.add_INSTANCE("waypoint","wp1")
    rosplan_library.add_INSTANCE("waypoint","wp2")
    rosplan_library.add_INSTANCE("waypoint","wp3")
    rosplan_library.add_INSTANCE("waypoint","wp4")

    #I set all hint as taken
    rosplan_library.add_FACT_predicate_single_param("hint_taken","waypoint","wp0",True)
    rosplan_library.add_FACT_predicate_single_param("hint_taken","waypoint","wp1",True)
    rosplan_library.add_FACT_predicate_single_param("hint_taken","waypoint","wp2",True)
    rosplan_library.add_FACT_predicate_single_param("hint_taken","waypoint","wp3",True)
    rosplan_library.add_FACT_predicate_single_param("hint_taken","waypoint","wp4",True)

    
    #I set waypoint wp0 as the home waypoint 
    rosplan_library.add_FACT_predicate_single_param("is_home","waypoint","wp0",True)


        #I set the robot position in the right waypoint
    rosplan_library.add_FACT_predicate_single_param("robot_at","waypoint",robot_at,True)


    #I know that I have already taken this hint so i consequently add this information inside the pddl 
    rosplan_library.add_FACT_predicate_single_param("hp_checked","waypoint","wp0",True)
    rosplan_library.add_FACT_predicate_single_param("hp_checked","waypoint",robot_at,True)

    #I will consider that all hps are already checked
    rosplan_library.add_FACT_predicate_NO_param("hps_checked",True)

    #I will ask the algorithm to test the hps
    rosplan_library.add_GOAL_predicate_NO_param("hps_tested",True)


        
    #Generete and parse the pddl
    rosplan_library.generate_the_problem_and_plan_and_parse()

    #Asking for the execution
    result=rosplan_library.dispatch_client()
    print(result)
def replan_until_you_have_a_complete_hint():
    ##
    #\brief This function will oblidge the robot to visit and take all the hints. 
    # Once the motion is completed if there is a new complete id it will test it.
    # It can also happen that the plan get interrupted by another node if there is the need to test 

    need_to_test=False
    
    #It will loop until there is the need to test 
    while(not need_to_test):

        #The plan gets deleted
        rosplan_library.clear_plan()

        #Here waypoints get initialized as instances inside the problem.pddl
        rosplan_library.add_INSTANCE("waypoint","wp0")
        rosplan_library.add_INSTANCE("waypoint","wp1")
        rosplan_library.add_INSTANCE("waypoint","wp2")
        rosplan_library.add_INSTANCE("waypoint","wp3")
        rosplan_library.add_INSTANCE("waypoint","wp4")

        #Here I receive which is the robot position in order to set it correctly
        robot_at = rospy.get_param('/robot_at')
        robot_at="wp"+str(robot_at)

        #I set waypoint wp0 as the home waypoint 
        rosplan_library.add_FACT_predicate_single_param("is_home","waypoint","wp0",True)

        #I set the hint of waypoint wp0 as taken and checked due to there is no hint to be taken in that position
        rosplan_library.add_FACT_predicate_single_param("hint_taken","waypoint","wp0",True)
        rosplan_library.add_FACT_predicate_single_param("hp_checked","waypoint","wp0",True)

        #I set the robot position in the right waypoint
        rosplan_library.add_FACT_predicate_single_param("robot_at","waypoint",robot_at,True)

        #I know that I have already taken this hint so i consequently add this information inside the pddl 
        rosplan_library.add_FACT_predicate_single_param("hp_checked","waypoint",robot_at,True)
        rosplan_library.add_FACT_predicate_single_param("hint_taken","waypoint",robot_at,True)

        #I will ask as goal that all the hps need to be checked. This means that it will take all the hints, and continsly check if there is a new complete id
        rosplan_library.add_GOAL_predicate_NO_param("hps_checked",True)

        #Generete and parse the pddl
        rosplan_library.generate_the_problem_and_plan_and_parse()

        #Asking for the execution
        result=rosplan_library.dispatch_client()
        print(result)

        #Here I will check if there is the need to test
        need_to_test = rospy.get_param('/hint_to_be_tested')
        if(need_to_test):
            print("Need to test!")
            time.sleep(1)
def main():
  ##
  #\brief This is the main, here there will be initialization and it will be executed a spin()
  global rosplan_library

  #Node initialization
  rospy.init_node('state_machine', anonymous=True)
  
  #Param used to comunicate and close other nodes
  all_hints_taken = rospy.set_param('/hint_to_be_tested',False)
  
  #Initialization of the library
  rosplan_library=my_rosplan_class()
  
  you_win=False

  #Until you have win we will continue to move around and do test
  while(not you_win):

    replan_until_you_have_a_complete_hint()
    plan_a_test()
    you_win = rospy.get_param('/you_win')

if __name__ == '__main__':
  main()
