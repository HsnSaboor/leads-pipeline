# Lead Generation Pipeline

CLI tool for automated lead generation from Google Maps with WhatsApp verification.

## Install

**Linux/macOS:**
```
curl -fsSL https://raw.githubusercontent.com/HsnSaboor/leads-pipeline/master/install.sh | sh
```

**Windows (PowerShell):**
```
irm "https://raw.githubusercontent.com/HsnSaboor/leads-pipeline/master/install.ps1" | iex
```

## Quick Start

```
# First time: download scraper binary
leads setup

# Create queries file
echo "Dentists in Lahore" > queries.txt

# Set API key (for WhatsApp verification)
export EVOLUTION_API_KEY="your_key"

# Run pipeline
leads run queries.txt
```

Output saved to `leads_output/final_leads.csv`

## Commands

| Command | Description |
|---------|-------------|
| `leads setup` | Download scraper binary |
| `leads run <file>` | Full pipeline: scrape, filter, verify |
| `leads scrape <file>` | Scrape Google Maps only |
| `leads filter <file>` | Filter leads by criteria |
| `leads check <file>` | Verify WhatsApp numbers |

## Options Explained

### Concurrency (`-c`)

Number of parallel browser instances scraping at once.

- Default: 8 (recommended for most machines)
- Higher = faster scraping, but needs more CPU and RAM
- Example: `-c 16` for powerful machines, `-c 4` for laptops

Performance with `-c 8`:
- ~120 places/minute
- ~1,600 places in 13 minutes

### Depth (`-d`)

Number of times to scroll down the results page.

- Default: 1 (fastest, gets ~16 results per query)
- Higher = more results, but slower
- Example: `-d 10` can get 100+ results per query

## Full Options

```
leads run <file> [options]

  -o, --output DIR      Where to save results (default: leads_output)
  -c, --concurrency N   Parallel workers (default: 8)
  -d, --depth N         Scroll depth (default: 1)
  -l, --lang LANG       Language code (default: en)
  --skip-whatsapp       Skip WhatsApp verification
```

```
leads scrape <file> [options]

  -o, --output FILE     Output CSV file (default: results.csv)
  -c, --concurrency N   Parallel workers (default: 8)
  -d, --depth N         Scroll depth (default: 1)
  -t, --timeout TIME    Exit after inactivity (default: 3m)
```

```
leads filter <file> [options]

  -o, --output FILE     Output file (default: filtered.csv)
  --no-website          Remove businesses with websites
  --keep-website        Keep all businesses
  --min-reviews N       Filter by minimum reviews
  --min-rating N        Filter by minimum rating
```

```
leads check <file> [options]

  -o, --output FILE     Output file (default: verified.csv)
  -b, --batch-size N    Numbers per API request (default: 50)
```

## Configuration

Create `.env` file or set environment variables:

```
EVOLUTION_API_KEY=your_key           # Required for WhatsApp check
EVOLUTION_API_URL=https://evoapi.botomation.tech
EVOLUTION_INSTANCE=demo
```

## Manual Install

```
uv tool install leads-pipeline
```

Or with pip:
```
pip install leads-pipeline
```

## Output Files

Running `leads run queries.txt` creates:

```
leads_output/
  raw_results.csv        All scraped businesses
  filtered_leads.csv     Businesses without websites
  final_leads.csv        With WhatsApp verification
```

## Data Fields

| Field | Description |
|-------|-------------|
| title | Business name |
| phone | Phone number |
| address | Full address |
| website | Website URL |
| rating | Star rating (0-5) |
| reviews | Number of reviews |
| category | Business type |
| latitude | GPS latitude |
| longitude | GPS longitude |
| whatsapp_exists | Has WhatsApp (true/false) |

## Examples

```
# Quick scrape
leads scrape queries.txt -c 8 -d 1

# Deep scrape with 16 workers
leads scrape queries.txt -c 16 -d 10

# Filter for quality leads
leads filter raw.csv --min-rating 4.0 --min-reviews 50

# Run without WhatsApp check
leads run queries.txt --skip-whatsapp
```

## Uninstall

```
uv tool uninstall leads-pipeline
rm -rf ~/.leads-pipeline
```

## Requirements

- Python 3.10+
- 64-bit Linux, macOS, or Windows

## License

MIT
