/**
* @file my_action.cpp
* @brief This files physically execute the pddl predicates
* @author Federico Zecchi
* @version 0.1
* @date 31/03/2022
*
* Clients : <BR>
* ° /oracle_solution
* ° /move_arm
* ° /hints_received_and_complete
* ° /cancel_dispatch
*
*/

#include "exp_ass2_moveit_4949035/my_action.h"
#include <unistd.h>
#include <actionlib/client/simple_action_client.h>
#include <actionlib/client/terminal_state.h>
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
	}

	bool MyActionInterface::concreteCallback(const rosplan_dispatch_msgs::ActionDispatch::ConstPtr& msg) {
	/**
	 * \brief This function become active when some particular predicates get executed
	 * 
	 * 
	 */
		int id_to_be_tested=-1;
		ros::NodeHandle nh("~");

		//Different code lines will be executed with different predicates
		if(msg->name=="goto_waypoint"){
			//If the predicate request to go to a waypoint, then we will speak to the action server "go_to_point_action" and request the motion
			std::cout << "Going from " << msg->parameters[0].value << " to " << msg->parameters[1].value << std::endl;
			
			actionlib::SimpleActionClient<rt2_ass1_ros1::go_to_pointAction> ac("/go_to_point_action", true);
			

			rt2_ass1_ros1::go_to_pointGoal goal;
			ac.waitForServer();
			
			//the msg->parameters[1] is the second parameter of the goto_waypoint predicate, it contains information about the goal waypoint
			//Then based on which waypoint we are referring we will plan a different xyz goal
			if(msg->parameters[1].value == "wp1"){
			goal.target_position.x= 2.5;
			goal.target_position.y = 0;
			goal.theta = 3.14;
			nh.setParam("/robot_at", 1);
			}
			else if (msg->parameters[1].value == "wp2"){
			goal.target_position.x= 0;
			goal.target_position.y = 2.5;
			goal.theta = -1.57;
			nh.setParam("/robot_at", 3);
			}
			else if (msg->parameters[1].value == "wp3"){
			goal.target_position.x= -2.5;
			goal.target_position.y = 0;
			goal.theta = 0;
			nh.setParam("/robot_at", 2);
			}
			else if (msg->parameters[1].value == "wp4"){
			goal.target_position.x= 0;
			goal.target_position.y = -2.5;
			goal.theta = 1.57;
			nh.setParam("/robot_at", 4);
			}
			else if (msg->parameters[1].value == "wp0"){
			goal.target_position.x= 0;
			goal.target_position.y = 0;
			goal.theta = 0;
			nh.setParam("/robot_at", 0);
			}
			ac.sendGoal(goal);
			ac.waitForResult();
			
			
			ROS_INFO("Action (%s) performed: completed!", msg->name.c_str());
			}
		else if(msg->name=="take_hint"){
				//This is the take_hint predicate, and will force the robotic arm to move by calling the "move_arm" client
				ROS_INFO("Taking hint");
				
				exp_ass2_moveit_4949035::comunication com;
				//I will comunicate in which waypoint is my target 
				com.request.msg1=msg->parameters[0].value;
				client_rp.call(com);
				ROS_INFO("Response: %s \n Success: %d",com.response.response,com.response.success);
			}
		else if(msg->name=="check_hp"){
			//This predicate get called after taking the hint and it will check if there is a complete id. 
			//In case there is a new complete id it will cancel the plan and comunicate that a test need to be performed 
			exp_ass2_moveit_4949035::comunication msg_complete_hints;
			
			//Here we ask to the ID_handler node through its server which ids are completed
			msg_complete_hints.request.msg1="hints_complete";
			client_check_hints.call(msg_complete_hints);
			
			cout<<endl<<endl<<endl;
			bool hint_to_be_tested=false;

			//Here we check if all there is a complete id which we have nedver tested
			for (int i=0;i<number_ids;i++) {
				//first we check if the id number i is complete. This information is inside the response message we received from the id_handler
				if(msg_complete_hints.response.data[i]==1){
					//then we check if the id has ever been tested
					if(tested_ids[i]==0){

						id_to_be_tested=i;
						
						//with this line we assure that we will never test it
						tested_ids[i]=1;

						//We set that the id i need to be tested
						nh.setParam("/id_to_be_tested", i);
						ROS_INFO("I will need to test the id:%d",i);

						//I force the cycle to exit
						i=number_ids+1;


						hint_to_be_tested=true;
						std_srvs::Empty empy_msg;

						//asking to stop the dispatch, this is performed due to there is no need to move to other waypoint before testing.
						//This means that the plan need to be stopped and a new one will be created by the state machine
						client_cancel_dispatch.call(empy_msg);
					}
				}
			}


				nh.setParam("/hint_to_be_tested", hint_to_be_tested);
			}
		else if(msg->name=="test_hp"){
			//With the activation of this predicate i will read from the param server which is the id to anylize.
			//I will ask to the "oracle_solution" server which is the winner id and compare it to the id i have found

			//Saving from the param server the id to be tested
			nh.getParam("/id_to_be_tested", id_to_be_tested);
			ROS_INFO("\n\nI want to test id:%d",id_to_be_tested);

			//If it is a valid id
			if(id_to_be_tested!=-1){

				//calling the "oracle_solution" server to know the winner id
				exp_ass2_moveit_4949035::Oracle solution;
				client_solution.call(solution);
				int sol=solution.response.ID;

				//If the two ids are the same then we have won
				if(sol==id_to_be_tested){
				nh.setParam("/you_win", true);
				ROS_INFO("YOU WIN!");
				}
				else{
				ROS_INFO("The id was not correct!");
				}

				//clearing the param server
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
		/**
		 *\brief This is the main function, here most of the initialization will be processed and then KCL will run
		 * 
		 * 
		 */
		
		//ros initialization
		ros::init(argc, argv, "my_rosplan_action", ros::init_options::AnonymousName);
		ros::NodeHandle nh("~");

		//Initializing rosparam server
		nh.setParam("/hint_to_be_tested", false);
		nh.setParam("/you_win", false);
		nh.setParam("/id_to_be_tested", -1);
		nh.setParam("/robot_at", 0);

		//Initialization of tested_ids array, this will help me to keep track of ids that I have already checked
		for (int i=0;i<number_ids;i++) {
			tested_ids[i]=0;
		}
		//Client initialization
		client_solution = nh.serviceClient<exp_ass2_moveit_4949035::Oracle>("/oracle_solution");
		client_rp = nh.serviceClient<exp_ass2_moveit_4949035::comunication>("/move_arm");
		client_check_hints = nh.serviceClient<exp_ass2_moveit_4949035::comunication>("/hints_received_and_complete");
		client_cancel_dispatch = nh.serviceClient<std_srvs::Empty>("/rosplan_plan_dispatcher/cancel_dispatch");
		
		//KCL initialization
		KCL_rosplan::MyActionInterface my_aci(nh);
		
		//Running KCL
		my_aci.runActionInterface();
		ROS_INFO("Action concluded");
		return 0;
	}

