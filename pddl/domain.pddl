(define (domain zecchi-domain)

(:requirements :strips :typing :fluents :disjunctive-preconditions :durative-actions :adl)

(:types
        waypoint
)

(:predicates
        (robot_at ?wp - waypoint)
        (hint_taken ?wp - waypoint)
        (hps_checked)
)



(:durative-action goto_waypoint
        :parameters (?from ?to - waypoint)
        :duration ( = ?duration 60)
        :condition (and
                (at start(robot_at ?from))
                )
        :effect (and
                (at end(robot_at ?to))
                (at start (not (robot_at ?from)))
                )

)

(:durative-action take_hint
        :parameters (?wp - waypoint)
        :duration ( = ?duration 60)
        :condition (at start(robot_at ?wp))
        :effect (at end( hint_taken ?wp))

)

(:durative-action check_hp
        :parameters(?wp - waypoint)
        :duration ( = ?duration 0)
        :condition (and
                                (at start (forall (?wp - waypoint) ( hint_taken ?wp)))
                                )
        :effect ( and
                        (at end (hps_checked))
                        )
)

)
