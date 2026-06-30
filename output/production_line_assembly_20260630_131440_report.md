# ETG schedule report - Production line assembly

Generated at: 2026-06-30T13:14:40
Mode: MinimizeTime

Scenario

A compact manufacturing workflow for checking material, cutting parts, assembly, quality control, packaging, and storage.

Summary

Total execution time: 14.07
Total cost: 1349.24
Average resource utilization: 19.3%

Schedule

p1 Material check: GT, 0 -> 1.11, Robot arm, cost 88.33
p2 Cut components: DT, 1.11 -> 3.61, Machine A, cost 190.00
p3 Automated assembly: CDT, 3.61 -> 7.02, Robot arm, Machine technician, cost 515.53
p4 Manual adjustment: GT, 7.02 -> 8.5, Robot arm, cost 121.11
p5 Quality control: DT, 8.5 -> 11, Quality inspector, cost 137.50
p6 Packaging: CGT, 11 -> 12.57, Machine A, Robot arm, cost 221.76
p7 Move to storage: DT, 12.57 -> 14.07, Forklift operator, cost 75.00

Resource usage

Machine A: busy 4.07, idle 10, utilization 28.9%, tasks 2
Robot arm: busy 7.57, idle 6.5, utilization 53.8%, tasks 4
Machine technician: busy 3.4, idle 10.66, utilization 24.2%, tasks 1
Quality inspector: busy 2.5, idle 11.57, utilization 17.8%, tasks 1
Forklift operator: busy 1.5, idle 12.57, utilization 10.7%, tasks 1
Universal worker 1: busy 0, idle 14.07, utilization 0.0%, tasks 0
Universal worker 2: busy 0, idle 14.07, utilization 0.0%, tasks 0
