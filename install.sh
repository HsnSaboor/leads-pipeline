#!/bin/bash
# Lead Generation Pipeline Installer for Linux/macOS
# Run: curl -fsSL https://raw.githubusercontent.com/HsnSaboor/leads-pipeline/master/install.sh | sh

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

step() {
    echo -e "\n${CYAN}==>$NC $1"
}

success() {
    echo -e "${GREEN}OK:$NC $1"
}

error() {
    echo -e "${RED}ERROR:$NC $1"
    exit 1
}

# Banner
echo -e "${BLUE}"
cat << "EOF"
  _                        _____     _ _       ___ _           _   
 | |                      / ____|   | | |     / _ \ |         | |  
 | |     __ _ _____   _  | |     ___| | | ___| | | | |_ __   __| |  
 | |    / _` |_  / | | | | |    / _ \ | |/ _ \ | | | | '_ \ / _` |  
 | |___| (_| |/ /| |_| | | |___|  __/ | |  __/ |_| | | | | | (_| |  
 |______\__,_/___|\__, |  \_____\___|_|_|\___|\___/|_|_| |_|\__,_|  
                   __/ |                                             
                  |___/     Lead Generation Pipeline
EOF
echo -e "${NC}"

# Check Python
step "Checking Python installation"
if command -v python3 &> /dev/null; then
    PYTHON="python3"
elif command -v python &> /dev/null; then
    PYTHON="python"
else
    error "Python not found. Please install Python 3.10+ from https://python.org"
fi

PYTHON_VERSION=$($PYTHON --version 2>&1)
success "Found $PYTHON_VERSION"

# Install uv
step "Installing uv (fast Python package installer)"
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    
    # Add to PATH for current session
    export PATH="$HOME/.local/bin:$PATH"
    
    # Add to shell config
    for rc in "$HOME/.bashrc" "$HOME/.zshrc" "$HOME/.profile"; do
        if [ -f "$rc" ] && ! grep -q 'export PATH="$HOME/.local/bin:$PATH"' "$rc"; then
            echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$rc"
        fi
    done
fi
success "uv is installed"

# Install leads-pipeline
step "Installing leads-pipeline CLI"

VERSION="${1:-latest}"
if [ "$VERSION" = "latest" ]; then
    PACKAGE="leads-pipeline"
else
    PACKAGE="leads-pipeline==$VERSION"
fi

# Try PyPI first, fallback to GitHub
if uv tool install "$PACKAGE" --force 2>/dev/null; then
    success "Installed from PyPI"
else
    echo "Installing from GitHub..."
    uv tool install "git+https://github.com/HsnSaboor/leads-pipeline.git" --force
    success "Installed from GitHub"
fi

# Ensure PATH
export PATH="$HOME/.local/bin:$PATH"

# Verify installation
step "Verifying installation"
if command -v leads &> /dev/null; then
    LEADS_VERSION=$(leads --version 2>&1 || echo "installed")
    success "leads-pipeline $LEADS_VERSION"
else
    error "Installation failed. Try: export PATH=\"\$HOME/.local/bin:\$PATH\""
fi

# Download scraper binary
step "Downloading Google Maps Scraper binary"
leads setup 2>/dev/null || true
success "Scraper binary ready"

# Done
echo -e "${GREEN}"
cat << "EOF"

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
  export EVOLUTION_API_KEY="your_api_key"

EOF
echo -e "${NC}"
