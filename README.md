# Lead Generation Pipeline

Automated lead generation for local businesses in Pakistan using Google Maps scraper and WhatsApp verification.

## Features

- **Google Maps Scraper**: Extract business leads (name, phone, address, website, ratings)
- **Filter**: Remove businesses that already have websites
- **WhatsApp Check**: Verify phone numbers using Evolution API

## Configuration

### 1. Evolution API Setup

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Edit `.env` with your values:
- `EVOLUTION_API_KEY` - Required. Get from your Evolution API instance
- `EVOLUTION_API_URL` - Optional. Default: `https://evoapi.botomation.tech`
- `EVOLUTION_INSTANCE` - Optional. Default: `demo`

Or set via environment variable:
```bash
export EVOLUTION_API_KEY=your_api_key_here
```

### 2. Python Environment

```bash
# Create virtual environment
uv venv .venv

# Activate
source .venv/bin/activate

# Install dependencies
uv pip install requests
```

## Quick Start

```bash
# Run full pipeline
cd leads-project
source .venv/bin/activate
export EVOLUTION_API_KEY=your_key_here
./run_pipeline.sh
```

## Manual Steps

```bash
# 1. Scrape (requires Docker)
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
export EVOLUTION_API_KEY=your_key_here
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

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `EVOLUTION_API_KEY` | Yes | - | API key for Evolution API |
| `EVOLUTION_API_URL` | No | `https://evoapi.botomation.tech` | Evolution API URL |
| `EVOLUTION_INSTANCE` | No | `demo` | Instance name to use |

## Output Files

- `raw_data/results.csv` - Raw scraped data
- `filtered_data/leads_without_website.csv` - Businesses without websites
- `filtered_data/final_leads.csv` - Final leads with WhatsApp status
