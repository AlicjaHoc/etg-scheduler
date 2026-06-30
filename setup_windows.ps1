$ErrorActionPreference = "Stop"

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host ""
Write-Host "Setup complete. Run the app with:"
Write-Host ".\.venv\Scripts\Activate.ps1"
Write-Host "python -m etg_scheduler"
