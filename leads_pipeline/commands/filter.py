"""Filter command."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from leads_pipeline.core import filter_leads

console = Console()


def filter_cmd(
    input_file: Path = typer.Argument(
        ...,
        exists=True,
        help="Path to input CSV file",
    ),
    output: Path = typer.Option(
        Path("filtered.csv"),
        "--output",
        "-o",
        help="Output CSV file",
    ),
    no_website: bool = typer.Option(
        True,
        "--no-website/--keep-website",
        help="Filter out businesses with websites",
    ),
    min_reviews: Optional[int] = typer.Option(
        None,
        "--min-reviews",
        help="Minimum number of reviews",
    ),
    min_rating: Optional[float] = typer.Option(
        None,
        "--min-rating",
        help="Minimum rating (0-5)",
    ),
) -> None:
    """Filter leads based on criteria."""
    console.print("[cyan]→[/cyan] Filtering leads...")

    count = filter_leads(
        input_file=input_file,
        output_file=output,
        remove_with_website=no_website,
        min_reviews=min_reviews,
        min_rating=min_rating,
    )

    console.print(f"[green]✓[/green] Filtered {count} leads to {output}")
