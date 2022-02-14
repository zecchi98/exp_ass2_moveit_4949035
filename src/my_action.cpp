#include "exp_ass2_moveit_4949035/my_action.h"
#include <unistd.h>
#include <actionlib/client/simple_action_client.h>
#include <actionlib/client/terminal_state.h>
//#include <motion_plan/PlanningAction.h>
#include "rt2_ass1_ros1/go_to_pointAction.h"
#include "exp_ass2_moveit_4949035/comunication.h"
#include "std_srvs/Empty.h"
ros::ServiceClient client_rp,client_check_hints,client_cancel_dispatch;
namespace KCL_rosplan {

	MyActionInterface::MyActionInterface(ros::NodeHandle &nh) {
			// here the initialization
	}

	bool MyActionInterface::concreteCallback(const rosplan_dispatch_msgs::ActionDispatch::ConstPtr& msg) {
			// here the implementation of the action

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

			exp_ass2_moveit_4949035::comunication com;
			com.request.msg1="hints_complete";
			client_check_hints.call(com);
		}
		else if(msg->name=="test_hp"){

			ROS_INFO("WE WILL REPLAN");
			std_srvs::Empty x;
			client_cancel_dispatch.call(x);

		}
		return true;
	}
}

	int main(int argc, char **argv) {
		ros::init(argc, argv, "my_rosplan_action", ros::init_options::AnonymousName);
		ros::NodeHandle nh("~");

   		client_rp = nh.serviceClient<exp_ass2_moveit_4949035::comunication>("/move_arm");
   		client_check_hints = nh.serviceClient<exp_ass2_moveit_4949035::comunication>("/hints_received_and_complete");
   		client_cancel_dispatch = nh.serviceClient<std_srvs::Empty>("/rosplan_plan_dispatcher/dispatch_plan");
		KCL_rosplan::MyActionInterface my_aci(nh);
		my_aci.runActionInterface();
		ROS_INFO("Action concluded");
		return 0;
	}

