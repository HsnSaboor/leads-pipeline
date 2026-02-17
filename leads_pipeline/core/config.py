"""Core configuration management."""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


class Config:
    def __init__(self, env_file: Optional[Path] = None):
        if env_file and env_file.exists():
            load_dotenv(env_file)
        else:
            load_dotenv()

        self.evolution_api_key: str = os.getenv("EVOLUTION_API_KEY", "")
        self.evolution_api_url: str = os.getenv(
            "EVOLUTION_API_URL", "https://evoapi.botomation.tech"
        )
        self.evolution_instance: str = os.getenv("EVOLUTION_INSTANCE", "demo")
        self.scraper_version: str = os.getenv("GOOGLE_MAPS_SCRAPER_VERSION", "v1.10.1")
        self.disable_telemetry: bool = os.getenv("DISABLE_TELEMETRY", "1") == "1"

    def validate(self) -> bool:
        return bool(self.evolution_api_key)

    def get_binary_dir(self) -> Path:
        return Path.home() / ".leads-pipeline" / "bin"

    def get_binary_path(self) -> Path:
        import platform

        system = platform.system().lower()
        binary_name = "google-maps-scraper.exe" if system == "windows" else "google-maps-scraper"
        return self.get_binary_dir() / binary_name

    def get_data_dir(self) -> Path:
        return Path.home() / ".leads-pipeline" / "data"

    def ensure_dirs(self) -> None:
        self.get_binary_dir().mkdir(parents=True, exist_ok=True)
        self.get_data_dir().mkdir(parents=True, exist_ok=True)
