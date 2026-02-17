# Lead Generation Pipeline Installer for Windows
# Run: irm "https://raw.githubusercontent.com/HsnSaboor/leads-pipeline/main/install.ps1" | iex

param(
    [string]$Version = "latest",
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host "`n==> $Message" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "OK: $Message" -ForegroundColor Green
}

function Write-Err {
    param([string]$Message)
    Write-Host "ERROR: $Message" -ForegroundColor Red
}

# Banner
Write-Host @"

  _                        _____     _ _       ___ _           _   
 | |                      / ____|   | | |     / _ \ |         | |  
 | |     __ _ _____   _  | |     ___| | | ___| | | | |_ __   __| |  
 | |    / _` |_  / | | | | |    / _ \ | |/ _ \ | | | | '_ \ / _` |  
 | |___| (_| |/ /| |_| | | |___|  __/ | |  __/ |_| | | | | | (_| |  
 |______\__,_/___|\__, |  \_____\___|_|_|\___|\___/|_|_| |_|\__,_|  
                   __/ |                                             
                  |___/     Lead Generation Pipeline

"@ -ForegroundColor Blue

# Check Python
Write-Step "Checking Python installation"
try {
    $pythonVersion = & $Python --version 2>&1
    Write-Success "Found $pythonVersion"
} catch {
    Write-Err "Python not found. Please install Python 3.10+ from https://python.org"
    exit 1
}

# Install uv if not present
Write-Step "Installing uv (fast Python package installer)"
try {
    $uvCmd = Get-Command uv -ErrorAction SilentlyContinue
    if (-not $uvCmd) {
        Write-Host "Installing uv via PowerShell..."
        irm https://astral.sh/uv/install.ps1 | iex
        # Refresh PATH
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "User") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "Machine")
    }
    Write-Success "uv is installed"
} catch {
    Write-Err "Failed to install uv: $_"
    exit 1
}

# Install leads-pipeline
Write-Step "Installing leads-pipeline CLI"
$Package = if ($Version -eq "latest") { "leads-pipeline" } else { "leads-pipeline==$Version" }

# Try PyPI first, fallback to git
try {
    & uv tool install $Package --force 2>&1 | Out-Null
    Write-Success "Installed from PyPI"
} catch {
    Write-Host "Installing from GitHub..."
    & uv tool install "git+https://github.com/botomation/leads-pipeline.git" --force 2>&1 | Out-Null
    Write-Success "Installed from GitHub"
}

# Verify installation
Write-Step "Verifying installation"
try {
    $leadsVersion = & leads --version 2>&1
    Write-Success "leads-pipeline $leadsVersion"
} catch {
    Write-Err "Installation verification failed"
    Write-Host "Try adding uv tools to PATH: `$env:Path += `"`$env:USERPROFILE\.local\bin`""
    exit 1
}

# Download scraper binary
Write-Step "Downloading Google Maps Scraper binary"
& leads setup 2>&1 | Out-Null
Write-Success "Scraper binary ready"

# Done
Write-Host @"

Installation complete! 

Quick start:
  leads --help           Show all commands
  leads setup            Download scraper binary
  leads run queries.txt  Run full pipeline

Example queries.txt:
  Dentists in Lahore
  Private Schools in Karachi
  Beauty Clinics in Islamabad

Configure WhatsApp API:
  $env:EVOLUTION_API_KEY = "your_api_key"

"@ -ForegroundColor Green
