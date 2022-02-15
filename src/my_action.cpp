#include "exp_ass2_moveit_4949035/my_action.h"
#include <unistd.h>
#include <actionlib/client/simple_action_client.h>
#include <actionlib/client/terminal_state.h>
//#include <motion_plan/PlanningAction.h>
#include "rt2_ass1_ros1/go_to_pointAction.h"
#include "exp_ass2_moveit_4949035/comunication.h"
#include "exp_ass2_moveit_4949035/Oracle.h"
#include "std_srvs/Empty.h"
#define number_ids 6
#include <iostream>
using namespace std;
ros::ServiceClient client_rp,client_check_hints,client_cancel_dispatch,client_solution;

int tested_ids[number_ids];

namespace KCL_rosplan {

	MyActionInterface::MyActionInterface(ros::NodeHandle &nh) {
			// here the initialization
	}

	bool MyActionInterface::concreteCallback(const rosplan_dispatch_msgs::ActionDispatch::ConstPtr& msg) {
			// here the implementation of the action
    int id_to_be_tested=-1;
    ros::NodeHandle nh("~");
		if(msg->name=="goto_waypoint"){
		std::cout << "Going from " << msg->parameters[0].value << " to " << msg->parameters[1].value << std::endl;
		
   		actionlib::SimpleActionClient<rt2_ass1_ros1::go_to_pointAction> ac("/go_to_point_action", true);
		
   		rt2_ass1_ros1::go_to_pointGoal goal;
		ac.waitForServer();
		if(msg->parameters[1].value == "wp1"){
		goal.target_position.x= 2.5;
		goal.target_position.y = 0;
		goal.theta = 3.14;
		}
		else if (msg->parameters[1].value == "wp2"){
		goal.target_position.x= -2.5;
		goal.target_position.y = 0;
		goal.theta = 0;
		}
		else if (msg->parameters[1].value == "wp3"){
		goal.target_position.x= 0;
		goal.target_position.y = 2.5;
		goal.theta = -1.57;
		}
		else if (msg->parameters[1].value == "wp4"){
		goal.target_position.x= 0;
		goal.target_position.y = -2.5;
		goal.theta = 1.57;
		}
		else if (msg->parameters[1].value == "wp0"){
		goal.target_position.x= 0;
		goal.target_position.y = 0;
		goal.theta = 0;
		}
		ac.sendGoal(goal);
		ac.waitForResult();
		
		
		ROS_INFO("Action (%s) performed: completed!", msg->name.c_str());
		}
		else if(msg->name=="take_hint"){

			ROS_INFO("Taking hint");
			
			exp_ass2_moveit_4949035::comunication com;
			com.request.msg1=msg->parameters[0].value;
			client_rp.call(com);
			ROS_INFO("Response: %s \n Success: %d",com.response.response,com.response.success);
		}
		else if(msg->name=="check_hp"){

      exp_ass2_moveit_4949035::comunication msg_complete_hints;
      msg_complete_hints.request.msg1="hints_complete";
      client_check_hints.call(msg_complete_hints);
      /*cout<<endl<<endl;
      for (int i=0;i<number_ids;i++) {
        cout<<tested_ids[i];
      }*/
      cout<<endl<<endl<<endl;

      for (int i=0;i<number_ids;i++) {
        //cout<<msg_complete_hints.response.data[i];
        if(msg_complete_hints.response.data[i]==1){
          if(tested_ids[i]==0){
            id_to_be_tested=i;
            tested_ids[i]=1;
            nh.setParam("/id_to_be_tested", i);
            ROS_INFO("I will need to test the id:%d",i);
            i=number_ids+1;//esco dal ciclo
          }
        }
      }


      nh.setParam("hint_to_be_tested", true);
		}
		else if(msg->name=="test_hp"){

      nh.getParam("/id_to_be_tested", id_to_be_tested);
      ROS_INFO("\n\nI want to test id:%d",id_to_be_tested);
      if(id_to_be_tested!=-1){
        exp_ass2_moveit_4949035::Oracle solution;
        client_solution.call(solution);
        int sol=solution.response.ID;
        if(sol==id_to_be_tested){
          ROS_INFO("YOU WIN!");
        }
        else{
          ROS_INFO("The id was not correct!");
        }
        nh.setParam("/id_to_be_tested", -1);
      }
      else {
        ROS_INFO("\n\nNothing to test");
      }

      //resetto in modo da non ripetere il test
      nh.setParam("hint_to_be_tested", false);
      id_to_be_tested=-1;
		}
		return true;
	}
}

	int main(int argc, char **argv) {
		ros::init(argc, argv, "my_rosplan_action", ros::init_options::AnonymousName);
    ros::NodeHandle nh("~");
    nh.setParam("hint_to_be_tested", false);
    nh.setParam("/id_to_be_tested", -1);
    for (int i=0;i<number_ids;i++) {
      tested_ids[i]=0;
    }
      client_solution = nh.serviceClient<exp_ass2_moveit_4949035::Oracle>("/oracle_solution");
   		client_rp = nh.serviceClient<exp_ass2_moveit_4949035::comunication>("/move_arm");
   		client_check_hints = nh.serviceClient<exp_ass2_moveit_4949035::comunication>("/hints_received_and_complete");
   		client_cancel_dispatch = nh.serviceClient<std_srvs::Empty>("/rosplan_plan_dispatcher/dispatch_plan");
		KCL_rosplan::MyActionInterface my_aci(nh);
		my_aci.runActionInterface();
		ROS_INFO("Action concluded");
		return 0;
	}

