# ETG schedule report - Logistics warehouse shift

Generated at: 2026-06-30T13:32:34
Algorithm: Greedy
Mode: MinimizeCost

Scenario

A warehouse shift with truck unloading, scanning, pallet movement, sorting, inventory update, and dispatch loading.

Summary

Total execution time: 17.72
Total cost: 976.40
Average resource utilization: 27.1%

Schedule

l1 Unload incoming truck: CGT, 0 -> 3.43, Temporary worker 1, Temporary worker 2, cost 167.43
l2 Scan items: DT, 3.43 -> 5.43, Warehouse clerk, cost 72.00
l3 Move pallets to buffer: CDT, 5.43 -> 7.81, Forklift operator 1, Warehouse clerk, cost 198.33
l4 Sort packages: CGT, 7.81 -> 11.93, Temporary worker 1, Temporary worker 2, Temporary worker 3, cost 271.41
l5 Update inventory: UT, 11.93 -> 13.59, Temporary worker 1, cost 41.67
l6 Prepare shipments: GT, 13.59 -> 15.82, Temporary worker 1, cost 58.89
l7 Load dispatch truck: CDT, 15.82 -> 17.72, Forklift operator 1, Warehouse clerk, cost 166.67

Resource usage

Warehouse clerk: busy 6.29, idle 11.44, utilization 35.5%, tasks 3
Forklift operator 1: busy 4.29, idle 13.44, utilization 24.2%, tasks 2
Forklift operator 2: busy 0, idle 17.72, utilization 0.0%, tasks 0
Shift coordinator: busy 0, idle 17.72, utilization 0.0%, tasks 0
Temporary worker 1: busy 11.44, idle 6.29, utilization 64.5%, tasks 4
Temporary worker 2: busy 7.55, idle 10.17, utilization 42.6%, tasks 2
Temporary worker 3: busy 4.12, idle 13.6, utilization 23.2%, tasks 1
