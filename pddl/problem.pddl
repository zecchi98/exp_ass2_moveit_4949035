(define (problem task)
(:domain sherlockbot-domain)
(:objects
   wp0 wp1 wp2 - waypoint
)
(:init
    (robot_at wp0)
    (hint_taken wp0)
)
(:goal
    (hps_checked)
)
)
