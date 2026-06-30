# ETG Schedule Report: Production line assembly

Generated at: 2026-06-30T12:50:25
Optimization mode: MinimizeTime

## Scenario

A compact manufacturing workflow for checking material, cutting parts, assembly, quality control, packaging, and storage.

## Summary

- Total execution time: 14.07
- Total cost: 1349.24
- Average resource utilization: 19.3%

## Schedule

| Task | Type | Start | Finish | Resources | Cost |
| --- | --- | ---: | ---: | --- | ---: |
| Material check | GT | 0 | 1.11 | Robot arm | 88.33 |
| Cut components | DT | 1.11 | 3.61 | Machine A | 190.00 |
| Automated assembly | CDT | 3.61 | 7.02 | Robot arm, Machine technician | 515.53 |
| Manual adjustment | GT | 7.02 | 8.5 | Robot arm | 121.11 |
| Quality control | DT | 8.5 | 11 | Quality inspector | 137.50 |
| Packaging | CGT | 11 | 12.57 | Machine A, Robot arm | 221.76 |
| Move to storage | DT | 12.57 | 14.07 | Forklift operator | 75.00 |

## Resource usage

| Resource | Busy time | Idle time | Utilization | Tasks |
| --- | ---: | ---: | ---: | ---: |
| Machine A | 4.07 | 10 | 28.9% | 2 |
| Robot arm | 7.57 | 6.5 | 53.8% | 4 |
| Machine technician | 3.4 | 10.66 | 24.2% | 1 |
| Quality inspector | 2.5 | 11.57 | 17.8% | 1 |
| Forklift operator | 1.5 | 12.57 | 10.7% | 1 |
| Universal worker 1 | 0 | 14.07 | 0.0% | 0 |
| Universal worker 2 | 0 | 14.07 | 0.0% | 0 |
