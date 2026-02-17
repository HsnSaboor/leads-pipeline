"""Lead filtering functionality."""

import csv
from pathlib import Path
from typing import Optional


def filter_leads(
    input_file: Path,
    output_file: Path,
    remove_with_website: bool = True,
    min_reviews: Optional[int] = None,
    min_rating: Optional[float] = None,
) -> int:
    output_file.parent.mkdir(parents=True, exist_ok=True)

    filtered_count = 0

    with open(input_file, newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames or []

        with open(output_file, "w", newline="", encoding="utf-8") as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                if remove_with_website and row.get("website", "").strip():
                    continue

                if min_reviews is not None:
                    try:
                        reviews = int(row.get("reviews", 0) or 0)
                        if reviews < min_reviews:
                            continue
                    except ValueError:
                        pass

                if min_rating is not None:
                    try:
                        rating = float(row.get("rating", 0) or 0)
                        if rating < min_rating:
                            continue
                    except ValueError:
                        pass

                writer.writerow(row)
                filtered_count += 1

    return filtered_count
