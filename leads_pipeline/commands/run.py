"""Run full pipeline command."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from leads_pipeline.core import (
    Config,
    check_whatsapp,
    download_binary,
    filter_leads,
    run_scraper,
)

console = Console()


def run(
    input_file: Path = typer.Argument(
        ...,
        exists=True,
        help="Path to queries file (one per line)",
    ),
    output_dir: Path = typer.Option(
        Path("leads_output"),
        "--output",
        "-o",
        help="Output directory",
    ),
    concurrency: int = typer.Option(
        8,
        "--concurrency",
        "-c",
        help="Scraper concurrency",
    ),
    depth: int = typer.Option(
        1,
        "--depth",
        "-d",
        help="Scraping depth",
    ),
    lang: str = typer.Option(
        "en",
        "--lang",
        "-l",
        help="Language",
    ),
    skip_whatsapp: bool = typer.Option(
        False,
        "--skip-whatsapp",
        help="Skip WhatsApp verification",
    ),
) -> None:
    """Run full lead generation pipeline."""
    config = Config()

    if not config.validate() and not skip_whatsapp:
        console.print("[red]✗[/red] EVOLUTION_API_KEY not set")
        console.print("Set via: export EVOLUTION_API_KEY=your_key")
        console.print("Or use --skip-whatsapp to skip verification")
        raise typer.Exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)
    raw_file = output_dir / "raw_results.csv"
    filtered_file = output_dir / "filtered_leads.csv"
    final_file = output_dir / "final_leads.csv"

    console.print("\n[bold blue]Lead Generation Pipeline[/bold blue]\n")

    table = Table(show_header=False)
    table.add_column("Key", style="cyan")
    table.add_column("Value")
    table.add_row("Input", str(input_file))
    table.add_row("Output", str(output_dir))
    table.add_row("Workers", str(concurrency))
    table.add_row("Depth", str(depth))
    console.print(table)
    console.print()

    # Step 1: Download binary if needed
    binary_path = config.get_binary_path()
    if not binary_path.exists():
        console.print("[yellow]Step 0: Downloading scraper binary...[/yellow]")
        download_binary(config)
        console.print()

    # Step 2: Scrape
    console.print(f"[cyan]Step 1: Scraping Google Maps...[/cyan]")
    success = run_scraper(
        config,
        input_file=input_file,
        output_file=raw_file,
        concurrency=concurrency,
        depth=depth,
        lang=lang,
    )
    if not success:
        console.print("[red]✗[/red] Scraping failed")
        raise typer.Exit(1)
    console.print(f"[green]✓[/green] Raw results: {raw_file}\n")

    # Step 3: Filter
    console.print("[cyan]Step 2: Filtering leads without websites...[/cyan]")
    count = filter_leads(raw_file, filtered_file, remove_with_website=True)
    console.print(f"[green]✓[/green] Filtered {count} leads: {filtered_file}\n")

    # Step 4: WhatsApp check
    if not skip_whatsapp:
        console.print("[cyan]Step 3: Checking WhatsApp numbers...[/cyan]")
        try:
            verified = check_whatsapp(config, filtered_file, final_file)
            console.print(f"[green]✓[/green] {verified} WhatsApp verified: {final_file}\n")
        except Exception as e:
            console.print(f"[yellow]![/yellow] WhatsApp check failed: {e}")
            console.print("Filtered leads saved without WhatsApp status")
            final_file = filtered_file
    else:
        final_file = filtered_file

    console.print("[bold green]Pipeline Complete![/bold green]")
    console.print(f"Final output: {final_file}")
