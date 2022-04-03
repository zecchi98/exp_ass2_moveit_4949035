(define (domain zecchi-domain)

(:requirements :strips :typing :fluents :disjunctive-preconditions :durative-actions :adl)

(:types
        waypoint
)

(:predicates

        ;Indicates the actual position of the robot
        (robot_at ?wp - waypoint)

        ;Indicates if the hint corresponding to a waypoint has been taken
        (hint_taken ?wp - waypoint)

        ;I use this predicate in order to distinguish the wp0 as a home waypoint
        (is_home ?wp - waypoint)

        ;Used to save that for a particular waypoint: it has been visited, the hint has been taken and a hp check has been performed
        (hp_checked ?wp - waypoint)

        ;This indicates that all hps have been checked
        (hps_checked)

        ;This indicates that a test has been performed
        (hps_tested)
)


; With this action i will force the robot to move from a waypoint to another one 
(:durative-action goto_waypoint
        :parameters (?from ?to - waypoint)
        :duration ( = ?duration 60)
        :condition (and
                (at start(robot_at ?from))
                (at start(hp_checked ?from))
                )
        :effect (and
                (at end(robot_at ?to))
                (at start (not (robot_at ?from)))
                )

)

; With this action i will force the robot to take the hint with the arm
(:durative-action take_hint
        :parameters (?wp - waypoint)
        :duration ( = ?duration 60)
        :condition (at start(robot_at ?wp))
        :effect (at end( hint_taken ?wp))

)

; With this action the system will check if after the taken hint there is a new complete id
(:durative-action check_hp
        :parameters(?wp - waypoint)
        :duration ( = ?duration 0)
        :condition (and (at start(hint_taken ?wp)))
        :effect ( and
                        (at end (hp_checked ?wp))
                        )
)

; With this action if and only if every single waypoint has been checked then hps_checked become true
(:durative-action all_hp_checked
        :parameters()
        :duration ( = ?duration 0)
        :condition (and
                                (at start (forall (?wp - waypoint) ( hp_checked ?wp)))
                                )
        :effect (and (at end (hps_checked)))
)

; With this action if and only if hps_checked is true and my position is in the home position then i can perform a final test
(:durative-action test_hp
        :parameters(?wp - waypoint)
        :duration ( = ?duration 0)
        :condition (and (at start(hps_checked))(at start(robot_at ?wp))(at start(is_home ?wp)))
        :effect ( and
                        (at end (hps_tested))
                        )
)


)
