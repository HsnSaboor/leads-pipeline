"""WhatsApp verification via Evolution API."""

import csv
from pathlib import Path
from typing import Optional

import requests

from .config import Config


def check_whatsapp(
    config: Config,
    input_file: Path,
    output_file: Path,
    batch_size: int = 50,
) -> int:
    if not config.evolution_api_key:
        raise ValueError("EVOLUTION_API_KEY not configured")

    output_file.parent.mkdir(parents=True, exist_ok=True)

    url = f"{config.evolution_api_url}/chat/whatsappNumbers/{config.evolution_instance}"
    headers = {
        "apikey": config.evolution_api_key,
        "Content-Type": "application/json",
    }

    verified_count = 0

    with open(input_file, newline="", encoding="utf-8") as infile:
        reader = csv.DictReader(infile)
        fieldnames = list(reader.fieldnames or []) + ["whatsapp_exists"]

        rows = list(reader)

    with open(output_file, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in range(0, len(rows), batch_size):
            batch = rows[i : i + batch_size]
            phones = []

            for row in batch:
                phone = row.get("phone", "").strip()
                if phone:
                    phones.append(phone)

            if not phones:
                for row in batch:
                    row["whatsapp_exists"] = "false"
                    writer.writerow(row)
                continue

            try:
                response = requests.post(
                    url,
                    headers=headers,
                    json={"numbers": phones},
                    timeout=30,
                )
                response.raise_for_status()
                results = response.json()

                phone_status = {}
                for result in results:
                    phone_status[result.get("jid", "").split("@")[0]] = result.get("exists", False)

                for row in batch:
                    phone = row.get("phone", "").strip()
                    exists = phone_status.get(phone, False)
                    row["whatsapp_exists"] = str(exists).lower()

                    if exists:
                        verified_count += 1

                    writer.writerow(row)

            except requests.RequestException:
                for row in batch:
                    row["whatsapp_exists"] = "error"
                    writer.writerow(row)

    return verified_count
