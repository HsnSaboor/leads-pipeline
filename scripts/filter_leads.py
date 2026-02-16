#!/usr/bin/env python3
"""
Filter leads - remove businesses that already have websites
"""

import csv
import sys


def filter_leads(input_file, output_file):
    count = 0
    filtered = 0

    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for row in rows:
            count += 1
            website = row.get("website", "").strip()

            # Keep only businesses without websites
            if not website or website.lower() in ["n/a", "none", "", "-"]:
                writer.writerow(row)
                filtered += 1

    print(f"Processed {count} leads")
    print(f"Filtered leads (no website): {filtered}")
    print(f"Output saved to: {output_file}")


if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "raw_data/results.csv"
    output_file = (
        sys.argv[2] if len(sys.argv) > 2 else "filtered_data/leads_without_website.csv"
    )
    filter_leads(input_file, output_file)
