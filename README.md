# exp_ass2_moveit_4949035

# How to build the project

1) Installa i seguenti pacchetti:

    git clone https://github.com/zecchi98/rt2_ass1_ros1.git
    git clone https://github.com/zecchi98/exp_ass2_moveit_4949035.git

2) Esegui catkin_make

3) Se qualche pacchetto moveit è mancante procedi come segue:
    sudo apt update
    sudo apt install ros-noetic-moveit

# How to run the project

In the first window launch :
    roslaunch exp_ass2_moveit_4949035 my_launch_first.launch 

In the second window launch :
    roslaunch exp_ass2_moveit_4949035 my_launch_second.launch

# What the first launcher will execute?
 1) All the packages reguarding moveit
 2) Everithing that will prepare pddl and rosplan to work
 3) simulation_node node, which has been developed by the professor.
 4) goToPoint node, which belongs to rt2_ass1_ros1 assigment. A package we developed for research track 2 the last year
 5) robot_control node, which will handle the arm movements


# What the second launcher will execute?
 1)id_handler node, which will handle and save all the ids found.
 2)state_machine node, which will correctly handle all the pddls files

# Component diagram
The component diagram here below 
![component_diagram](https://user-images.githubusercontent.com/78590047/168242991-2aa84b73-a066-41ad-b9cf-307ef4492d22.png)


# How this project works?

This section is the most important one, here i will explain how every node interact which each other.
The state machine is mainly handled by rosplan, the state_machine node is used only to inizialize them. Indeed when the project is launched this node the problems.pddl by setting the actual position of the robot and as goal hps_checked which will force the robot to go to all the hint and to collect them.
Once this rosplan request is executed, the robot will start moving to the first position, this will be executed by the pddl_action "goto_waypoint" which will ask to rt2_ass1_ros1 package to handle the movement.
When the position is reached the pddl_action terminate and the "take_hint" pddl_action is executed. This one will call robot_control and ask him to handle the movement, in particular it will try to move up and down the robot arm in order to try to reach the hint.
After this step it will be executed "check_hp" pddl_action, which will call id_handler to know if there is a complete hypothesis. In case there is a complete hypothesis(which means that we need to check if it is the winner one) rosplan get interrupt and the plan deleted.
When all the places have been visited "check_hps" becomes true and the state_machine will ask for another round until there is a complete hypothesis.
As already said, if a complete hypothesis is found the plan get deleted and the state_machine will know of this thanks to "hint_to_be_tested" rosparam. In this step the state_machine will modify the problem.pddl to force the robot to "test_hp", it will then go to the center of the map and will call "/oracle_solution" service to know if the hp found is the winner one.
If it is not the winner id, then the state_machine will ask to continue finding ids.
Here below there is a state machine diagram of what i have already explained.
![state_machine](https://user-images.githubusercontent.com/78590047/168242897-da5b19ce-decd-41fd-b79f-5cbcbb0fb3b0.png)

# Topic explanation
The following topics are created by me:
    1) hint_to_be_tested, rosparam used to understand if there is a complete hint to be tested. It is used from the state_machine and from my_action.

    2) you_win, rosparam used to understand if the match is over. It is used by my_action and the state_machine
    
    3) id_to_be_tested, rosparam used to understand which is the id to be tested. It is used from my_action and the id_handler

    4) robot_at, rosparam used to understand which is the robot actual position. It is used from the state_machine and my_action

    5) oracle_solution, service used to know which is the id of the solution. my_action has a client of that topic

    6) move_arm, service used to request a movement of the arm. It is used from my_action to ask to robot_control to move the arm to a specific position. In particular my_action will comunicate the position of the robot and robot_control will use this information to elaborate the best position for the arm

    7) hints_received_and_complete, service used by my_action to request the list of all completed hints to the id_handler.

    8) go_to_point_action, topic used for an action comunication. my_action will request to goToPoint to move the robot in a particular position of the map
    
    9) oracle_hint, id_handler subscribes to this topic to know which ids are published.





# PDDL DOMAIN

Here i will explain which is the main structure of the pddl domain. For more information the domain.pddl has been commented.

The robot can move freely into the map.

If the robot is in a waypoint than it can freely take the hint.

If the robot is in a waypoint and the hint has been taken, then hp_check can be performed. This will be used in order to check if there is a complete id. If that is the case, it will stop the plan and after it will be requested to perform a test.

In order to know which is the home position i have created the (is_home ?wp - waypoint) predicate

if the robot is in the home position and all the hps are checked then a test can be performed

hps_checked will become true if and only if all the hp have been checked

hps_tested will become true if a test has been performed

# PDDL PROBLEM

The pddl problem will be generated from code, in particular from the state_machine.py file. Two main problem will be handled.

For both of the problem:
All the waypoint are initialized and wp0 is distinguished as the home waypoint through the appropriate predicate. At wp0 hp are consider as checked.
Every single time the problem is generated robot_at predicate will be set with the right position of the robot.

Here below the two types:

1) The first type of problem is used to move the robot around and collect hints, in particular the goal will be to get hps_checked TRUE. After that, the plan will terminate and the state machine will decide if another round is necessary or if it is necessary to do a test.

2)The second type of problem is used to perform a test. The goal will be to have hps_tested==TRUE, in order to complete this goal the robot will need to go to the home position and perform a test. After that, the plan will terminate and the state machine will decide if another round is necessary or if it is the end of the game.
hps_checked is initialized as TRUE.


# Documentation

if you want to know more about every single script, you can read the doxygen documentation, which can be found in the html folder 
