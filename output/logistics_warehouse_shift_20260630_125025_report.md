# ETG Schedule Report: Logistics warehouse shift

Generated at: 2026-06-30T12:50:25
Optimization mode: MinimizeCost

## Scenario

A warehouse shift with truck unloading, scanning, pallet movement, sorting, inventory update, and dispatch loading.

## Summary

- Total execution time: 17.72
- Total cost: 976.40
- Average resource utilization: 27.1%

## Schedule

| Task | Type | Start | Finish | Resources | Cost |
| --- | --- | ---: | ---: | --- | ---: |
| Unload incoming truck | CGT | 0 | 3.43 | Temporary worker 1, Temporary worker 2 | 167.43 |
| Scan items | DT | 3.43 | 5.43 | Warehouse clerk | 72.00 |
| Move pallets to buffer | CDT | 5.43 | 7.81 | Forklift operator 1, Warehouse clerk | 198.33 |
| Sort packages | CGT | 7.81 | 11.93 | Temporary worker 1, Temporary worker 2, Temporary worker 3 | 271.41 |
| Update inventory | UT | 11.93 | 13.59 | Temporary worker 1 | 41.67 |
| Prepare shipments | GT | 13.59 | 15.82 | Temporary worker 1 | 58.89 |
| Load dispatch truck | CDT | 15.82 | 17.72 | Forklift operator 1, Warehouse clerk | 166.67 |

## Resource usage

| Resource | Busy time | Idle time | Utilization | Tasks |
| --- | ---: | ---: | ---: | ---: |
| Warehouse clerk | 6.29 | 11.44 | 35.5% | 3 |
| Forklift operator 1 | 4.29 | 13.44 | 24.2% | 2 |
| Forklift operator 2 | 0 | 17.72 | 0.0% | 0 |
| Shift coordinator | 0 | 17.72 | 0.0% | 0 |
| Temporary worker 1 | 11.44 | 6.29 | 64.5% | 4 |
| Temporary worker 2 | 7.55 | 10.17 | 42.6% | 2 |
| Temporary worker 3 | 4.12 | 13.6 | 23.2% | 1 |
