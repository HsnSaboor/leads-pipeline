#!/usr/bin/env python3
"""
WhatsApp Number Validator using Evolution API
Fast, free, no browser automation
"""

import csv
import re
import sys
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

EVOLUTION_API_URL = "https://evoapi.botomation.tech"
EVOLUTION_API_KEY = "429683C4C977415CAAFCCE10F7D57E11"
INSTANCE_NAME = "demo"


def format_pakistani_phone(phone):
    """Convert Pakistani phone numbers to WhatsApp format (without +)"""
    digits = re.sub(r"\D", "", phone)

    if digits.startswith("92"):
        return digits
    elif digits.startswith("0"):
        return "92" + digits[1:]
    elif len(digits) == 10:
        return "92" + digits
    elif len(digits) == 11 and digits.startswith("0"):
        return "92" + digits[1:]
    else:
        return digits


def check_whatsapp_api(numbers_list):
    """Check multiple numbers at once using Evolution API"""
    url = f"{EVOLUTION_API_URL}/chat/whatsappNumbers/{INSTANCE_NAME}"
    headers = {"Content-Type": "application/json", "apikey": EVOLUTION_API_KEY}
    body = {"numbers": numbers_list}

    try:
        resp = requests.post(url, json=body, headers=headers, timeout=30)
        if resp.status_code == 200:
            return resp.json()
        return None
    except requests.RequestException:
        return None


def check_whatsapp(phone):
    """Check if a single number exists on WhatsApp"""
    formatted = format_pakistani_phone(phone)
    wa_url = f"https://wa.me/{formatted}"

    if len(formatted) < 11:
        return "INVALID", wa_url

    result = check_whatsapp_api([formatted])

    if result and len(result) > 0:
        exists = result[0].get("exists", False)
        return "YES" if exists else "NO", wa_url

    return "ERROR", wa_url


def process_leads(input_file, output_file, max_workers=15, batch_size=50):
    """Process all leads and check WhatsApp status"""

    with open(input_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        original_fields = list(reader.fieldnames)
        fieldnames = original_fields + ["wa_link", "wa_status"]
        rows = list(reader)

    print(f"Checking {len(rows)} numbers on WhatsApp...")

    phones_to_check = []
    for row in rows:
        phone = row.get("phone", "").strip()
        if phone:
            phones_to_check.append(phone)

    unique_phones = list(set(phones_to_check))
    print(f"Unique phones to check: {len(unique_phones)}")

    results = {}

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i in range(0, len(unique_phones), batch_size):
            batch = unique_phones[i : i + batch_size]
            result = check_whatsapp_api(batch)

            if result:
                for item in result:
                    phone = item.get("number", "")
                    exists = item.get("exists", False)
                    wa_url = f"https://wa.me/{phone}"
                    results[phone] = ("YES" if exists else "NO", wa_url)

            processed = min(i + batch_size, len(unique_phones))
            print(f"Processed {processed}/{len(unique_phones)}...")

    for row in rows:
        phone = row.get("phone", "").strip()
        phone_formatted = format_pakistani_phone(phone)

        if phone_formatted in results:
            status, wa_link = results[phone_formatted]
            row["wa_link"] = wa_link
            row["wa_status"] = status
        elif phone:
            row["wa_link"] = f"https://wa.me/{phone_formatted}"
            row["wa_status"] = "ERROR"
        else:
            row["wa_link"] = ""
            row["wa_status"] = "NO_PHONE"

    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    yes_count = sum(1 for r in rows if r.get("wa_status") == "YES")
    no_count = sum(1 for r in rows if r.get("wa_status") == "NO")
    error_count = sum(1 for r in rows if r.get("wa_status") in ["ERROR", "INVALID"])

    print(f"\n=== Results ===")
    print(f"On WhatsApp: {yes_count}")
    print(f"Not on WhatsApp: {no_count}")
    print(f"Errors: {error_count}")
    print(f"Output: {output_file}")


if __name__ == "__main__":
    input_file = (
        sys.argv[1] if len(sys.argv) > 1 else "filtered_data/leads_without_website.csv"
    )
    output_file = sys.argv[2] if len(sys.argv) > 2 else "filtered_data/final_leads.csv"
    process_leads(input_file, output_file)
