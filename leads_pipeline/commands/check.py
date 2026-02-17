"""Check WhatsApp command."""

from pathlib import Path

import typer
from rich.console import Console

from leads_pipeline.core import Config, check_whatsapp

console = Console()


def check(
    input_file: Path = typer.Argument(
        ...,
        exists=True,
        help="Path to input CSV file",
    ),
    output: Path = typer.Option(
        Path("verified.csv"),
        "--output",
        "-o",
        help="Output CSV file",
    ),
    batch_size: int = typer.Option(
        50,
        "--batch-size",
        "-b",
        help="Numbers to check per request",
    ),
) -> None:
    """Verify WhatsApp numbers via Evolution API."""
    config = Config()

    if not config.validate():
        console.print("[red]✗[/red] EVOLUTION_API_KEY not set")
        console.print("Set it via environment variable or .env file")
        raise typer.Exit(1)

    console.print("[cyan]→[/cyan] Checking WhatsApp numbers...")
    console.print(f"  API: {config.evolution_api_url}")
    console.print(f"  Instance: {config.evolution_instance}")

    try:
        count = check_whatsapp(
            config,
            input_file=input_file,
            output_file=output,
            batch_size=batch_size,
        )
        console.print(f"[green]✓[/green] Found {count} WhatsApp numbers in {output}")
    except Exception as e:
        console.print(f"[red]✗[/red] WhatsApp check failed: {e}")
        raise typer.Exit(1)
