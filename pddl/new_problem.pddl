(define (problem task)
(:domain zecchi-domain)
(:objects
    wp0 wp1 wp2 wp3 wp4 - waypoint
)
(:init
    (robot_at wp2)

    (hint_taken wp0)
    (hint_taken wp1)
    (hint_taken wp2)
    (hint_taken wp3)
    (hint_taken wp4)

    (is_home wp0)

    (hp_checked wp0)
    (hp_checked wp2)

    (hps_checked)


)
(:goal (and
    (hps_tested)
))
)
