"""Main CLI entry point."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from leads_pipeline import __version__

app = typer.Typer(
    name="leads",
    help="CLI tool for automated lead generation from Google Maps with WhatsApp verification",
    add_completion=False,
)

console = Console()


def version_callback(value: bool) -> None:
    if value:
        console.print(f"leads-pipeline version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        False,
        "--version",
        "-V",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit",
    ),
) -> None:
    """Lead Generation Pipeline CLI."""
    pass


@app.command("setup")
def setup_cmd(
    version: Optional[str] = typer.Option(
        None, "--version", "-v", help="Scraper version to download"
    ),
    force: bool = typer.Option(False, "--force", "-f", help="Force re-download"),
) -> None:
    """Download Google Maps Scraper binary."""
    from leads_pipeline.commands.install import install

    install(version, force)


@app.command("run")
def run_cmd(
    input_file: Path = typer.Argument(..., exists=True, help="Path to queries file"),
    output_dir: Path = typer.Option(
        Path("leads_output"), "--output", "-o", help="Output directory"
    ),
    concurrency: int = typer.Option(8, "--concurrency", "-c", help="Scraper workers"),
    depth: int = typer.Option(1, "--depth", "-d", help="Scraping depth"),
    lang: str = typer.Option("en", "--lang", "-l", help="Language"),
    skip_whatsapp: bool = typer.Option(False, "--skip-whatsapp", help="Skip WhatsApp check"),
) -> None:
    """Run full lead generation pipeline."""
    from leads_pipeline.commands.run import run

    run(input_file, output_dir, concurrency, depth, lang, skip_whatsapp)


@app.command("scrape")
def scrape_cmd(
    input_file: Path = typer.Argument(..., exists=True, help="Path to queries file"),
    output: Path = typer.Option(Path("results.csv"), "--output", "-o", help="Output file"),
    concurrency: int = typer.Option(8, "--concurrency", "-c", help="Workers"),
    depth: int = typer.Option(1, "--depth", "-d", help="Depth"),
    lang: str = typer.Option("en", "--lang", "-l", help="Language"),
    timeout: str = typer.Option("3m", "--timeout", "-t", help="Exit after inactivity"),
) -> None:
    """Run Google Maps scraper."""
    from leads_pipeline.commands.scrape import scrape

    scrape(input_file, output, concurrency, depth, lang, timeout)


@app.command("filter")
def filter_command(
    input_file: Path = typer.Argument(..., exists=True, help="Input CSV file"),
    output: Path = typer.Option(Path("filtered.csv"), "--output", "-o", help="Output file"),
    no_website: bool = typer.Option(
        True, "--no-website/--keep-website", help="Filter businesses with websites"
    ),
    min_reviews: Optional[int] = typer.Option(None, "--min-reviews", help="Minimum reviews"),
    min_rating: Optional[float] = typer.Option(None, "--min-rating", help="Minimum rating"),
) -> None:
    """Filter leads based on criteria."""
    from leads_pipeline.commands.filter import filter_cmd

    filter_cmd(input_file, output, no_website, min_reviews, min_rating)


@app.command("check")
def check_command(
    input_file: Path = typer.Argument(..., exists=True, help="Input CSV file"),
    output: Path = typer.Option(Path("verified.csv"), "--output", "-o", help="Output file"),
    batch_size: int = typer.Option(50, "--batch-size", "-b", help="Numbers per request"),
) -> None:
    """Verify WhatsApp numbers via Evolution API."""
    from leads_pipeline.commands.check import check

    check(input_file, output, batch_size)


if __name__ == "__main__":
    app()
