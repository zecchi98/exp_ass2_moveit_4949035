(define (problem task)
(:domain sherlockbot-domain)
(:objects
   wp0 wp1 wp2 wp3 wp4 - waypoint
)
(:init
    (robot_at wp0)
    (hint_taken wp0)
    (is_home wp0)
)
(:goal
    (hps_checked)
)
)
