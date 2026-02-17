"""Scrape command."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from leads_pipeline.core import Config, run_scraper

console = Console()


def scrape(
    input_file: Path = typer.Argument(
        ...,
        exists=True,
        help="Path to input file with queries (one per line)",
    ),
    output: Path = typer.Option(
        Path("results.csv"),
        "--output",
        "-o",
        help="Output CSV file",
    ),
    concurrency: int = typer.Option(
        8,
        "--concurrency",
        "-c",
        help="Number of concurrent workers",
    ),
    depth: int = typer.Option(
        1,
        "--depth",
        "-d",
        help="Scraping depth (scroll count)",
    ),
    lang: str = typer.Option(
        "en",
        "--lang",
        "-l",
        help="Language for results",
    ),
    timeout: str = typer.Option(
        "3m",
        "--timeout",
        "-t",
        help="Exit after inactivity (e.g., 3m, 5m)",
    ),
) -> None:
    """Run Google Maps scraper."""
    config = Config()

    console.print("[cyan]→[/cyan] Starting scraper...")
    console.print(f"  Input: {input_file}")
    console.print(f"  Output: {output}")
    console.print(f"  Workers: {concurrency}")

    success = run_scraper(
        config,
        input_file=input_file,
        output_file=output,
        concurrency=concurrency,
        depth=depth,
        lang=lang,
        exit_on_inactivity=timeout,
    )

    if success:
        console.print(f"[green]✓[/green] Scraping complete: {output}")
    else:
        console.print("[red]✗[/red] Scraping failed")
        raise typer.Exit(1)
