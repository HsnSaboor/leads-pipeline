# Lead Generation Pipeline

Automated lead generation for local businesses in Pakistan using Google Maps scraper and WhatsApp verification.

## Features

- **Google Maps Scraper**: Extract business leads (name, phone, address, website, ratings)
- **Filter**: Remove businesses that already have websites
- **WhatsApp Check**: Verify phone numbers using Evolution API

## Quick Start

```bash
# Run full pipeline
cd leads-project
./run_pipeline.sh
```

## Requirements

- Docker
- Python 3.x with `requests` (use venv)
- Evolution API (pre-configured)

## Manual Steps

```bash
# 1. Scrape
docker run --rm \
  -v "$PWD/queries:/queries" \
  -v "$PWD/raw_data/results.csv:/results.csv" \
  gosom/google-maps-scraper:latest-rod \
  -c 8 -depth 1 -lang en \
  -input /queries/target_queries.txt \
  -results /results.csv \
  -exit-on-inactivity 3m

# 2. Filter leads without websites
source .venv/bin/activate
python3 scripts/filter_leads.py raw_data/results.csv filtered_data/leads.csv

# 3. Check WhatsApp
python3 scripts/check_whatsapp.py filtered_data/leads.csv filtered_data/final_leads.csv
```

## Target Queries

Edit `queries/target_queries.txt` to customize:
- Private Schools
- Dental Clinics
- Beauty Clinics
- Dermatology Clinics
- Manufacturers (Surgical, Sports, Clothing)

## Performance

- ~120 places/minute with `-c 8 -depth 1`
- Rod browser (faster startup)
- Batch WhatsApp checking (50 numbers/request)
