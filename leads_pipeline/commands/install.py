"""Install command - download scraper binary."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from leads_pipeline.core import Config, download_binary

console = Console()


def install(
    version: Optional[str] = typer.Option(
        None, "--version", "-v", help="Scraper version to download"
    ),
    force: bool = typer.Option(False, "--force", "-f", help="Force re-download"),
) -> None:
    """Download Google Maps Scraper binary."""
    config = Config()
    binary_path = config.get_binary_path()

    if binary_path.exists() and not force:
        console.print(f"[green]✓[/green] Binary already installed at {binary_path}")
        console.print("Use --force to re-download")
        return

    if force and binary_path.exists():
        binary_path.unlink()

    download_binary(config, version)
    console.print("[green]✓[/green] Setup complete!")
    console.print("\nRun 'leads run --help' to start scraping")
