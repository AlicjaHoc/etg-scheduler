# ETG Scheduler

ETG Scheduler is a Python console application for an academic Extended Task Graph scheduling project.

The program loads a scenario from JSON, validates the task graph and resource constraints, creates a schedule with a greedy list scheduling algorithm, prints simple console output, and exports the result to JSON, CSV, and Markdown.

## Features

- Extended Task Graph model with dependencies between tasks
- Five task types: `DT`, `GT`, `UT`, `CDT`, `CGT`
- Universal and specialized resources
- Resource cost and speed multiplier support
- Validation of missing dependencies, cycles, task rules, and resource compatibility
- Three optimization modes: `MinimizeTime`, `MinimizeCost`, `Balanced`
- Simple console interface with menus, lists, and timeline output
- Example hospital, production line, and logistics warehouse scenarios
- Export to `output/` as JSON, CSV, and Markdown report
- Tests for validation, scheduling, and example scenarios

## Requirements

- Python 3.11 or Python 3.12
- Local virtual environment
- `pytest` from `requirements.txt` if you want to run tests

## Quick Start

### Windows

```bat
setup_windows.bat
run_app.bat
```

PowerShell users can also run:

```powershell
.\setup_windows.ps1
.\.venv\Scripts\Activate.ps1
python -m etg_scheduler
```

### macOS or Linux

```bash
cd ~/etg-scheduler
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m etg_scheduler
```

On Linux systems such as Pop!_OS or Ubuntu, the global command may be `python3` instead of `python`. After the virtual environment is activated, use `python` because it points to `.venv/bin/python`.

For later runs:

```bash
cd ~/etg-scheduler
source .venv/bin/activate
python -m etg_scheduler
```

## Command-Line Usage

Interactive mode:

```bash
source .venv/bin/activate
python -m etg_scheduler
```

Run a specific scenario:

```bash
source .venv/bin/activate
python -m etg_scheduler --scenario scenarios/hospital.json
```

Run a specific scenario and optimization mode:

```bash
python -m etg_scheduler --scenario scenarios/production_line.json --mode MinimizeTime
python -m etg_scheduler --scenario scenarios/logistics_warehouse.json --mode MinimizeCost
python -m etg_scheduler --scenario scenarios/hospital.json --mode Balanced
```

Show help:

```bash
python -m etg_scheduler --help
```

## Visual Studio Setup

1. Open Visual Studio.
2. Install the Python development workload if it is not installed.
3. Choose `Open a local folder`.
4. Select this project folder.
5. Open the Python Environments window.
6. Create or select a virtual environment in `.venv`.
7. Install dependencies from `requirements.txt`.
8. Run the module `etg_scheduler` or open a terminal inside Visual Studio and run:

```bat
python -m etg_scheduler
```

The project does not require a database, web server, GUI framework, or .NET runtime.

## Project Structure

```text
etg-scheduler/
  etg_scheduler/
    app.py
    __main__.py
    models/
    services/
    utilities/
  scenarios/
    hospital.json
    production_line.json
    logistics_warehouse.json
  output/
  tests/
  README.md
  README_FOR_STUDENT_PL.md
  SETUP.md
  requirements.txt
  pyproject.toml
  run_app.bat
  setup_windows.bat
  setup_windows.ps1
```

## Scenario Format

A scenario contains:

- `name`
- `description`
- `default_optimization_mode`
- `tasks`
- `resources`

Each task contains:

- `id`
- `name`
- `task_type`
- `duration`
- `dependencies`
- `required_specializations`
- `required_resource_count`
- `base_cost`
- `description`

Each resource contains:

- `id`
- `name`
- `resource_type`
- `specialization`
- `cost_per_time_unit`
- `speed_multiplier`

## Task Types

`DT` means Dedicated Task. It requires one specialized resource with a required specialization.

`GT` means General Task. It requires one resource. The resource may be universal or specialized.

`UT` means Universal Task. It requires one universal resource.

`CDT` means Common Dedicated Task. It requires multiple specialized resources at the same time.

`CGT` means Common General Task. It requires multiple resources of any type at the same time.

## Algorithm

The scheduler uses greedy list scheduling:

1. Load and validate the scenario.
2. Track scheduled tasks and resource availability.
3. Find all ready tasks whose dependencies are already scheduled.
4. Generate compatible resource assignments for ready tasks.
5. Calculate earliest start time, finish time, adjusted duration, and cost.
6. Select the best candidate according to the chosen optimization mode.
7. Add the selected task to the schedule.
8. Update the availability time of assigned resources.
9. Repeat until every task is scheduled.

The algorithm is intentionally explainable and practical for an academic console project. It is not intended to be a mathematically optimal solver.

## Output

Every successful run creates three files in `output/`:

- `*_schedule.json`
- `*_schedule.csv`
- `*_report.md`

The filenames include the scenario name and timestamp.

## Tests

Run tests after installing dependencies:

```bash
pytest
```

or:

```bash
python -m pytest
```
