# ETG Schedule Report: Hospital treatment workflow

Generated at: 2026-06-30T12:50:15
Optimization mode: Balanced

## Scenario

A small hospital process from registration through examination, laboratory work, surgery, recovery, and discharge.

## Summary

- Total execution time: 14.32
- Total cost: 2007.28
- Average resource utilization: 25.0%

## Schedule

| Task | Type | Start | Finish | Resources | Cost |
| --- | --- | ---: | ---: | --- | ---: |
| Patient registration | GT | 0 | 1 | Laboratory technician | 45.00 |
| Initial examination | DT | 1 | 3 | Dr Ewa Zielinska | 160.00 |
| Blood analysis | DT | 3 | 6 | Laboratory technician | 150.00 |
| Surgery preparation | CDT | 3 | 4.5 | Nurse Marek, Operating room 1 | 297.50 |
| Surgery | CDT | 6 | 9.87 | Dr Anna Nowak, Nurse Marek, Operating room 1 | 1206.45 |
| Recovery monitoring | UT | 9.87 | 13.2 | Universal assistant 1 | 110.00 |
| Discharge documents | GT | 13.2 | 14.32 | Universal assistant 1 | 38.33 |

## Resource usage

| Resource | Busy time | Idle time | Utilization | Tasks |
| --- | ---: | ---: | ---: | ---: |
| Dr Anna Nowak | 3.87 | 10.44 | 27.0% | 1 |
| Dr Ewa Zielinska | 2 | 12.32 | 14.0% | 1 |
| Nurse Marek | 5.37 | 8.94 | 37.5% | 2 |
| Laboratory technician | 4 | 10.32 | 27.9% | 2 |
| Operating room 1 | 5.37 | 8.94 | 37.5% | 2 |
| Universal assistant 1 | 4.44 | 9.87 | 31.0% | 2 |
| Universal assistant 2 | 0 | 14.32 | 0.0% | 0 |
