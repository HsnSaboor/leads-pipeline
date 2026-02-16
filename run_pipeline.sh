#!/bin/bash
# Run Lead Generation Pipeline - Best Performance Settings

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/scripts"
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate virtual environment
if [ -f "$PROJECT_DIR/.venv/bin/activate" ]; then
    source "$PROJECT_DIR/.venv/bin/activate"
else
    echo "Virtual environment not found. Run: uv venv .venv && uv pip install requests"
    exit 1
fi

echo "=== Lead Generation Pipeline ==="
echo "Performance: Rod browser, c=8, depth=1"
echo ""

# Step 1: Check for Docker
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is required but not installed"
    exit 1
fi

# Step 2: Run Google Maps Scraper
echo "Step 1: Running Google Maps Scraper..."
echo ""

touch "$PROJECT_DIR/raw_data/results.csv"

# Best performance settings:
# - latest-rod: Faster container startup (Chromium vs Playwright)
# - c 8: High concurrency (~120 places/minute)
# - depth 1: Fast scraping (minimum scrolls)
# - lang en: English results
# - exit-on-inactivity 3m: Auto-stop when no new results
DISABLE_TELEMETRY=1 docker run \
  --rm \
  -v "$PROJECT_DIR/queries:/queries" \
  -v "$PROJECT_DIR/raw_data/results.csv:/results.csv" \
  gosom/google-maps-scraper:latest-rod \
  -c 8 \
  -depth 1 \
  -lang en \
  -input /queries/target_queries.txt \
  -results /results.csv \
  -exit-on-inactivity 3m

echo ""
echo "Scraping complete!"
echo ""

# Step 3: Filter leads without websites
echo "Step 2: Filtering leads without websites..."
python3 "$SCRIPT_DIR/filter_leads.py" \
  "$PROJECT_DIR/raw_data/results.csv" \
  "$PROJECT_DIR/filtered_data/leads_without_website.csv"

echo ""

# Step 4: Check WhatsApp numbers
echo "Step 3: Checking WhatsApp numbers..."
python3 "$SCRIPT_DIR/check_whatsapp.py" \
  "$PROJECT_DIR/filtered_data/leads_without_website.csv" \
  "$PROJECT_DIR/filtered_data/final_leads.csv"

echo ""
echo "=== Pipeline Complete ==="
echo "Final leads: $PROJECT_DIR/filtered_data/final_leads.csv"
