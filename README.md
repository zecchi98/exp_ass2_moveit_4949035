# exp_ass2_moveit_4949035

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
