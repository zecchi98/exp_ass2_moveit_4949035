#!/usr/bin/env python
## @package exp_ass2_moveit_4949035
# \file ID_handler.py
# \brief This node will handle ids, it will wait for them on the topic and it will save them.
# It also has a service used to comunicate how many ids are completed
# \author Federico Zecchi
# \version 0.1
# \date 30/03/22
#
# \details
#
# Subscribes to: <BR>
# [/oracle_hint]
#
# Client : <BR>
# [/oracle_hint]
#
# Service : <BR>
# [/hints_received_and_complete]
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
 
class hypothesis_general():
    ##
    #\class hypothesis_general
    #\brief struct to handle hypothesis made of people,places,weapons and hypothesis_code. All this values are arrays, which not happen in the "hypothesis" class
    def __init__(self):
        ##
        #\brief init value to initialize arrays 
        super(hypothesis_general, self).__init__()
        self.people=[]
        self.places=[]
        self.weapons=[]
        self.hypothesis_code="HP-1"      
    def print_data(self):
        ##
        #\brief print data function
        print("\nhypo_code:")
        print(self.hypothesis_code)
        print("\npeople:")
        print(self.people)
        print("\nplaces:")
        print(self.places)
        print("\nweapons:")
        print(self.weapons)
    def add_person(self,person):
        ##
        #\brief add_person function
      if len(self.people)==0:
        self.people.append(person)
    def add_weapon(self,weapon):
        ##
        #\brief add_weapon function
      if len(self.weapons)==0:
        self.weapons.append(weapon)
    def add_place(self,place):
        ##
        #\brief add_place function
      if len(self.places)==0:
        self.places.append(place)
    def check_complete_and_consistent(self):
        ##
        #\brief check if the hypothesis is complete
      if len(self.weapons)==1 and len(self.people)==1 and len(self.places)==1:
        return True
      else:
        return False
    def set_hypo_code(self,hypo_code):
        ##
        #\brief set_hypo_code
      self.hypothesis_code=hypo_code
def callback_oracle_hint(req):
  ##
  #\brief This function is the callback from the "oracle_hint" topic. 
  global hypothesis
  


  #If there is no valid hint then nothing will happen
  if(req.value=='-1'):
      print("Not a valid hint")
      return
  #I save the id code
  hypothesis[req.ID].set_hypo_code(req.ID)

  #Then i will check what type of hint it is and consequently save the hint.
  if req.key=="where":
    hypothesis[req.ID].add_place(req.value)
  if req.key=="who":
    hypothesis[req.ID].add_person(req.value)
  if req.key=="what":
    hypothesis[req.ID].add_weapon(req.value)
  print("hint received")
  hypothesis[req.ID].print_data()
def callback_service_hints_received_and_complete(req):
  ##
  #\brief This function is the callback from the "hints_received_and_complete" service. It can be requested to know which hints are complete.
  #The response will contain all the hints completed inside the response.data array

  #We prepare the response to the service request
  response=comunicationResponse()
  response.response="ok"
  response.success=True

  #The response.data array will specify which ids are complete
  response.data=[0,0,0,0,0,0]

  #If the request is related to which hints are completed then we will modify the response.data
  if req.msg1=="hints_complete":
    for i in range(0,6):
      if(hypothesis[i].check_complete_and_consistent()):
        response.data[i]=1
  return response
def define_all_initial_functions():
    ##
    #\brief This function is used to define and initialize
    global hypothesis

    #Inizialization of the ros node
    rospy.init_node('id_handler', anonymous=True)

    #Inizialization of hypothesis array
    hypothesis=[]
    for i in range(0,6):
      hypothesis.append(hypothesis_general())
    
    #Initialization of the Subscriber and the server
    rospy.Subscriber("/oracle_hint", ErlOracle, callback_oracle_hint)
    rospy.Service("/hints_received_and_complete",comunication,callback_service_hints_received_and_complete)
def main():
  ##
  #\brief This is the main, here it will be called the "define_all_initial_functions" and it will be executed a spin()
  
  #Defining initial functions
  define_all_initial_functions()
  
  #It's pretty much the same as using rospy.spin()
  try:
    while (not rospy.core.is_shutdown()):
        rospy.rostime.wallsleep(0.5)
  except rospy.ROSInterruptException:
    return
  except KeyboardInterrupt:
    return

  except bool_exit==True:
      return
if __name__ == '__main__':
  main()
