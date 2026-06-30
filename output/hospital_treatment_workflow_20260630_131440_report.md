# ETG schedule report - Hospital treatment workflow

Generated at: 2026-06-30T13:14:40
Mode: Balanced

Scenario

A small hospital process from registration through examination, laboratory work, surgery, recovery, and discharge.

Summary

Total execution time: 14.32
Total cost: 2007.28
Average resource utilization: 25.0%

Schedule

h1 Patient registration: GT, 0 -> 1, Laboratory technician, cost 45.00
h2 Initial examination: DT, 1 -> 3, Dr Ewa Zielinska, cost 160.00
h3 Blood analysis: DT, 3 -> 6, Laboratory technician, cost 150.00
h4 Surgery preparation: CDT, 3 -> 4.5, Nurse Marek, Operating room 1, cost 297.50
h5 Surgery: CDT, 6 -> 9.87, Dr Anna Nowak, Nurse Marek, Operating room 1, cost 1206.45
h6 Recovery monitoring: UT, 9.87 -> 13.2, Universal assistant 1, cost 110.00
h7 Discharge documents: GT, 13.2 -> 14.32, Universal assistant 1, cost 38.33

Resource usage

Dr Anna Nowak: busy 3.87, idle 10.44, utilization 27.0%, tasks 1
Dr Ewa Zielinska: busy 2, idle 12.32, utilization 14.0%, tasks 1
Nurse Marek: busy 5.37, idle 8.94, utilization 37.5%, tasks 2
Laboratory technician: busy 4, idle 10.32, utilization 27.9%, tasks 2
Operating room 1: busy 5.37, idle 8.94, utilization 37.5%, tasks 2
Universal assistant 1: busy 4.44, idle 9.87, utilization 31.0%, tasks 2
Universal assistant 2: busy 0, idle 14.32, utilization 0.0%, tasks 0
