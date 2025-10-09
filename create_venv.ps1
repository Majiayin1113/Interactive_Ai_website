<#
Creates a Python virtual environment and installs dependencies.
Usage (PowerShell):
  .\create_venv.ps1 -VenvName .venv
Parameters:
  -VenvName: Name or path of venv folder to create (default: .venv)
  -Python: Optional path to python executable (default: python)
#>

param(
  [string]$BaseDir = "F:\\PolyU\\Sem1\\5913Programming",
  [string]$VenvName = $null,
  [string]$Python = "python"
)

# Determine venv path (default: <BaseDir>/.venv)
if (-not $VenvName) {
  $VenvPath = Join-Path $BaseDir ".venv"
} else {
  $VenvPath = $VenvName
}

Write-Host "Creating virtual environment '$VenvPath' using python: $Python"

& $Python -m venv $VenvPath
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to create virtual environment. Ensure Python is installed and on PATH."
    exit 1
}

$activate = Join-Path $VenvPath "Scripts/Activate.ps1"
if (-Not (Test-Path $activate)) {
    Write-Error "Activation script not found at $activate"
    exit 1
}

Write-Host "Activating venv and installing dependencies..."
& powershell -NoProfile -ExecutionPolicy Bypass -Command "& '$activate'; python -m pip install --upgrade pip; pip install -r requirements.txt"

Write-Host "Done. To activate the venv in your current session run:`n& '$activate'"
