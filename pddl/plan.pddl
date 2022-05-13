Number of literals: 17
Constructing lookup tables: [10%] [20%] [30%] [40%] [50%] [60%] [70%] [80%] [90%] [100%] [110%] [120%]
Post filtering unreachable actions:  [10%] [20%] [30%] [40%] [50%] [60%] [70%] [80%] [90%] [100%] [110%] [120%]
[01;34mNo analytic limits found, not considering limit effects of goal-only operators[00m
All the ground actions in this problem are compression-safe
Initial heuristic = 13.000
b (12.000 | 60.000)b (11.000 | 120.001)b (10.000 | 120.002)b (9.000 | 180.003)b (8.000 | 240.004)b (7.000 | 240.005)b (6.000 | 300.006)b (5.000 | 360.007)b (4.000 | 360.008)b (3.000 | 420.009)b (2.000 | 480.010)b (1.000 | 480.011);;;; Solution Found
; States evaluated: 14
; Cost: 480.012
; Time 0.00
0.000: (goto_waypoint wp0 wp1)  [60.000]
60.001: (take_hint wp1)  [60.000]
120.002: (check_hp wp1)  [0.000]
120.003: (goto_waypoint wp1 wp2)  [60.000]
180.004: (take_hint wp2)  [60.000]
240.005: (check_hp wp2)  [0.000]
240.006: (goto_waypoint wp2 wp3)  [60.000]
300.007: (take_hint wp3)  [60.000]
360.008: (check_hp wp3)  [0.000]
360.009: (goto_waypoint wp3 wp4)  [60.000]
420.010: (take_hint wp4)  [60.000]
480.011: (check_hp wp4)  [0.000]
480.012: (all_hp_checked)  [0.000]
