#!/usr/bin/env python3
#fold all: ctrl + k + 0
#unfold all: ctrl + k + j
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
flagMiddlePanelCreated=False
bool_exit=False

class my_rosplan_class():
  def __init__(self):
    super(my_rosplan_class, self).__init__()
    print("Waiting for services")
    rospy.wait_for_service("rosplan_knowledge_base/update")
    rospy.wait_for_service("rosplan_knowledge_base/clear")
    rospy.wait_for_service("rosplan_problem_interface/problem_generation_server")
    rospy.wait_for_service("rosplan_planner_interface/planning_server")
    rospy.wait_for_service("rosplan_parsing_interface/parse_plan")
    rospy.wait_for_service("rosplan_plan_dispatcher/cancel_dispatch")
    rospy.wait_for_service("rosplan_plan_dispatcher/dispatch_plan")
    print("All services ready")
    self.clear_plan=rospy.ServiceProxy('/rosplan_knowledge_base/clear',Empty)
    self.update_the_plan=rospy.ServiceProxy('/rosplan_knowledge_base/update',KnowledgeUpdateService)
    self.generate_problem_client=rospy.ServiceProxy('/rosplan_problem_interface/problem_generation_server',Empty)
    self.planning_server_client=rospy.ServiceProxy('/rosplan_planner_interface/planning_server',Empty)
    self.parse_plan_client=rospy.ServiceProxy('/rosplan_parsing_interface/parse_plan',Empty)
    self.cancel_dispatch_client=rospy.ServiceProxy('/rosplan_plan_dispatcher/cancel_dispatch',Empty)
    self.dispatch_client=rospy.ServiceProxy('/rosplan_plan_dispatcher/dispatch_plan',DispatchService)
    self.debug=True
  def clear_plan(self):
    self.clear_plan()
  def add_GOAL_predicate_single_param(self,predicate_name,key,value,bool):
    #key is the type while value is the name of the variable
    #bool is used to set to True or False the goal
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
    #key is the type while value is the name of the variable
    #bool is used to set to True or False the goal
    req=KnowledgeUpdateServiceRequest()
    req.knowledge.is_negative=not(bool)
    req.update_type=1
    req.knowledge.knowledge_type=1
    req.knowledge.attribute_name=predicate_name
    result=self.update_the_plan(req)
    if self.debug==True:
      print(result)
  def add_INSTANCE(self,type,name):
    #key is the type while value is the name of the variable
    #bool is used to set to True or False the goal
    req=KnowledgeUpdateServiceRequest()

    req.update_type=0
    req.knowledge.knowledge_type=0
    req.knowledge.instance_name=name
    req.knowledge.instance_type=type
    result=self.update_the_plan(req)
    if self.debug==True:
      print(result)
  def add_FACT_predicate_single_param(self,predicate_name,key,value,bool):
    #key is the type while value is the name of the variable
    #bool is used to set to True or False the goal
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
    #key is the type while value is the name of the variable
    #bool is used to set to True or False the goal
    req=KnowledgeUpdateServiceRequest()
    req.knowledge.is_negative=not(bool)
    req.update_type=0
    req.knowledge.knowledge_type=1
    req.knowledge.attribute_name=predicate_name
    result=self.update_the_plan(req)
    if self.debug==True:
      print(result)
  def generate_the_problem_and_plan_and_parse(self):
    self.generate_problem_client()
    self.planning_server_client()
    self.parse_plan_client()
  def cancel_dispatch(self):
    self.cancel_dispatch_client()
  def dispatch_plan(self):
    return self.dispatch_client()


def callback_oracle_hint(req):
  global hypothesis
  # int32 ID;  string key; string value
  hypothesis[req.ID].set_hypo_code(req.ID)
  if req.key=="where":
    hypothesis[req.ID].add_place(req.value)

  if req.key=="who":
    hypothesis[req.ID].add_person(req.value)

  if req.key=="what":
    hypothesis[req.ID].add_weapon(req.value)
  print("hint received")
  hypothesis[req.ID].print_data()
def callback_service_hints_received_and_complete(req):
  response=comunicationResponse()
  response.response="ok"
  response.success=True
  response.data=[0,0,0,0,0,0]
  if req.msg1=="hints_complete":
    for i in range(0,6):
      if(hypothesis[i].check_complete_and_consistent()):
        response.data[i]=1
  print(response)
  return response

def define_all_initial_functions():
    global rosplan_library
    rospy.init_node('state_machine', anonymous=True)
    bool_exit=False


    rosplan_library=my_rosplan_class()
    rosplan_library.generate_the_problem_and_plan_and_parse()
    result=rosplan_library.dispatch_client()
    print(result)
    print("FINITO, ORA LO FACCIO RIPARTIRE")

    rosplan_library.cancel_dispatch()
    rosplan_library.clear_plan()

    rosplan_library.add_INSTANCE("waypoint","wp0")
    rosplan_library.add_INSTANCE("waypoint","wp1")
    #rosplan_library.add_INSTANCE("waypoint","wp3")
    #rosplan_library.add_INSTANCE("waypoint","wp4")

    rosplan_library.add_FACT_predicate_single_param("hint_taken","waypoint","wp0",True)
    
    rosplan_library.add_FACT_predicate_single_param("robot_at","waypoint","wp0",True)

    #Let's set the goal
    rosplan_library.add_GOAL_predicate_NO_param("HP_tested",True)




    rosplan_library.generate_the_problem_and_plan_and_parse()
    rosplan_library.generate_the_problem_and_plan_and_parse()
    result=rosplan_library.dispatch_client()
    print(result)


    rosplan_library.generate_the_problem_and_plan_and_parse()
    rosplan_library.generate_the_problem_and_plan_and_parse()
    result=rosplan_library.dispatch_client()
    print(result)

    
def prova():
    nul=0

def main():
  define_all_initial_functions()
  try:
    while (not rospy.core.is_shutdown()) and (not bool_exit):
        rospy.rostime.wallsleep(0.5)
        #rospy.spin()
  except rospy.ROSInterruptException:
    return
  except KeyboardInterrupt:
    return

  except bool_exit==True:
      return
if __name__ == '__main__':
  main()
