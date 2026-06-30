# ETG schedule report - Water power plant building process

Generated at: 2026-06-30T13:31:22
Algorithm: Genetic
Mode: MinimizeCost
Time constraint: 48
Constraint status: OK

Scenario

A simplified extended task graph for building a small hydroelectric power plant. The genetic scheduler searches for a low-cost assignment of tasks to resources while keeping the total project time under the time constraint.

Summary

Total execution time: 47.99
Total cost: 12576.23
Average resource utilization: 12.0%

Schedule

w1 Prepare construction site: CGT, 0 -> 4.76, Fast crane operator, General construction team 1, cost 914.29
w2 Survey river bed: DT, 4.76 -> 8.76, Survey team, cost 430.00
w3 Build temporary cofferdam: CDT, 8.76 -> 14.72, Senior civil engineer, Fast crane operator, cost 1780.85
w4 Pour concrete foundation: CDT, 14.72 -> 22.16, Senior civil engineer, Concrete team, cost 2537.21
w5 Install water intake gate: CDT, 22.16 -> 26.92, Basic mechanical engineer, Fast crane operator, cost 1259.52
w8 Build control room: GT, 22.16 -> 26.87, General construction team 2, cost 535.29
w6 Install turbine: CDT, 26.92 -> 32.78, Basic mechanical engineer, Turbine specialist team, cost 1970.73
w7 Install generator: CDT, 32.78 -> 37.65, Electrical engineer, Generator specialist team, cost 1700.00
w9 Connect control system: DT, 37.65 -> 41.65, Automation engineer, cost 710.00
w10 Safety inspection: DT, 41.65 -> 44.65, Safety inspector, cost 435.00
w11 Trial operation: UT, 44.65 -> 47.99, General construction team 1, cost 303.33

Resource usage

Senior civil engineer: busy 13.4, idle 34.59, utilization 27.9%, tasks 2
Junior civil engineer: busy 0, idle 47.99, utilization 0.0%, tasks 0
Survey team: busy 4, idle 43.99, utilization 8.3%, tasks 1
Fast crane operator: busy 15.48, idle 32.51, utilization 32.3%, tasks 3
Basic crane operator: busy 0, idle 47.99, utilization 0.0%, tasks 0
Concrete team: busy 7.44, idle 40.55, utilization 15.5%, tasks 1
Senior mechanical engineer: busy 0, idle 47.99, utilization 0.0%, tasks 0
Basic mechanical engineer: busy 10.62, idle 37.37, utilization 22.1%, tasks 2
Turbine specialist team: busy 5.85, idle 42.13, utilization 12.2%, tasks 1
Electrical engineer: busy 4.88, idle 43.11, utilization 10.2%, tasks 1
Generator specialist team: busy 4.88, idle 43.11, utilization 10.2%, tasks 1
Automation engineer: busy 4, idle 43.99, utilization 8.3%, tasks 1
Safety inspector: busy 3, idle 44.99, utilization 6.3%, tasks 1
General construction team 1: busy 8.1, idle 39.89, utilization 16.9%, tasks 2
General construction team 2: busy 4.71, idle 43.28, utilization 9.8%, tasks 1
