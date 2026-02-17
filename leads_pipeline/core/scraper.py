"""Google Maps Scraper management."""

import platform
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.progress import BarColumn, Progress, TextColumn, TimeRemainingColumn

from .config import Config

console = Console()

BASE_URL = "https://github.com/gosom/google-maps-scraper/releases/download"


def get_system_info() -> tuple[str, str]:
    system = platform.system().lower()
    machine = platform.machine().lower()

    if machine in ("x86_64", "amd64"):
        arch = "amd64"
    elif machine in ("arm64", "aarch64"):
        arch = "arm64"
    else:
        arch = machine

    return system, arch


def get_binary_url(version: str) -> str:
    system, arch = get_system_info()
    ext = ".exe" if system == "windows" else ""
    filename = f"google_maps_scraper-1.10.1-rod-{system}-{arch}{ext}"
    return f"{BASE_URL}/{version}/{filename}"


def download_binary(config: Config, version: Optional[str] = None) -> Path:
    version = version or config.scraper_version
    binary_path = config.get_binary_path()
    config.ensure_dirs()

    if binary_path.exists():
        console.print(f"[green]✓[/green] Binary already exists at {binary_path}")
        return binary_path

    url = get_binary_url(version)
    console.print(f"[cyan]→[/cyan] Downloading Google Maps Scraper...")
    console.print(f"  Version: {version}")
    console.print(f"  URL: {url}")

    try:
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("Downloading", total=None)

            def hook(block_num: int, block_size: int, total_size: int) -> None:
                if total_size > 0:
                    progress.update(task, total=total_size, completed=block_num * block_size)

            urllib.request.urlretrieve(url, binary_path, hook)

        binary_path.chmod(0o755)
        console.print(f"[green]✓[/green] Downloaded to {binary_path}")
        return binary_path

    except Exception as e:
        console.print(f"[red]✗[/red] Download failed: {e}")
        sys.exit(1)


def run_scraper(
    config: Config,
    input_file: Path,
    output_file: Path,
    concurrency: int = 8,
    depth: int = 1,
    lang: str = "en",
    exit_on_inactivity: str = "3m",
) -> bool:
    binary_path = config.get_binary_path()

    if not binary_path.exists():
        console.print("[yellow]Binary not found. Downloading...[/yellow]")
        download_binary(config)

    output_file.parent.mkdir(parents=True, exist_ok=True)

    env = {}
    if config.disable_telemetry:
        env["DISABLE_TELEMETRY"] = "1"

    cmd = [
        str(binary_path),
        "-c",
        str(concurrency),
        "-depth",
        str(depth),
        "-lang",
        lang,
        "-input",
        str(input_file),
        "-results",
        str(output_file),
        "-exit-on-inactivity",
        exit_on_inactivity,
    ]

    console.print(f"[cyan]→[/cyan] Running scraper with {concurrency} workers...")

    try:
        result = subprocess.run(
            cmd,
            env={**dict(__import__("os").environ), **env},
            check=False,
        )
        return result.returncode == 0
    except Exception as e:
        console.print(f"[red]✗[/red] Scraper failed: {e}")
        return False
