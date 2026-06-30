# Setup Guide

This project is a Python console application. It should be run inside a local virtual environment.

## Windows Command Prompt

```bat
setup_windows.bat
run_app.bat
```

Manual setup:

```bat
python -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m etg_scheduler
```

## Windows PowerShell

```powershell
.\setup_windows.ps1
.\.venv\Scripts\Activate.ps1
python -m etg_scheduler
```

If PowerShell blocks script execution, run this for the current session:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```

Then run the setup script again.

## Visual Studio

1. Install Visual Studio with the Python development workload.
2. Open this folder with `File > Open > Folder`.
3. In Python Environments, create a virtual environment named `.venv`.
4. Install dependencies from `requirements.txt`.
5. Open the Visual Studio terminal.
6. Run:

```bat
python -m etg_scheduler
```

You can also run a scenario directly:

```bat
python -m etg_scheduler --scenario scenarios\hospital.json --mode Balanced
```

## Visual Studio Code

1. Open the project folder in VS Code.
2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Select `.venv` as the Python interpreter.
4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Run:

```bash
python -m etg_scheduler
```

## macOS or Linux

```bash
cd ~/etg-scheduler
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m etg_scheduler
```

On Pop!_OS and Ubuntu, `python` may not exist globally. That is fine. Use `python3` to create the virtual environment, then activate it. After activation, use `python`.

Later runs only need:

```bash
cd ~/etg-scheduler
source .venv/bin/activate
python -m etg_scheduler
```

## Useful Commands

Interactive run:

```bash
source .venv/bin/activate
python -m etg_scheduler
```

Run hospital scenario:

```bash
source .venv/bin/activate
python -m etg_scheduler --scenario scenarios/hospital.json --mode Balanced
```

Run the water power plant scenario with the genetic algorithm:

```bash
source .venv/bin/activate
python -m etg_scheduler --scenario scenarios/water_power_plant.json --algorithm genetic
```

Run tests:

```bash
pytest
```

Clean generated output manually by deleting generated files from `output/`. Keep `output/.gitkeep` if you want the folder to remain in Git.
