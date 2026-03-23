#!/usr/bin/env python3
"""
Update nca.txt from FuseNCA fuses.json
Fetches the latest firmware NCA database from https://github.com/sthetix/FuseNCA
and converts it to NxNandManager's nca.txt format.
"""

import json
import urllib.request
import os

# URLs
FUSENCA_URL = "https://raw.githubusercontent.com/sthetix/FuseNCA/master/fuses.json"

# Output path (relative to script location)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "..", "nca.txt")

# Title IDs
TITLE_ID_SYSTEM_VERSION = "0100000000000809"  # SystemVersion
TITLE_ID_EXFAT = "010000000000081B"            # BootImagePackageExFat

# Header for nca.txt
NCA_HEADER = """# NxNandManager NCA Database
# Format: [NCA] <firmware_version> <nca_filename> <title_id>
# This file is automatically updated from FuseNCA fuses.json
# Source: https://github.com/sthetix/FuseNCA
#
# Title IDs:
#   0100000000000809 = SystemVersion (used for firmware version detection)
#   010000000000081B = BootImagePackageExFat (used for exFAT driver detection)

"""


def parse_version_tuple(v_str):
    """
    Parse version string like "21.2.0" into a tuple (21, 2, 0) for sorting.
    Handles various version formats safely.
    """
    try:
        parts = v_str.split('.')
        return tuple(int(p) for p in parts)
    except (ValueError, AttributeError):
        # Fallback for non-standard version strings
        return (0, 0, 0)


def fetch_fuses_json():
    """Fetch the fuses.json from FuseNCA repository."""
    print(f"Fetching {FUSENCA_URL}...")
    with urllib.request.urlopen(FUSENCA_URL) as response:
        return json.loads(response.read().decode('utf-8'))


def convert_to_nca_txt(data):
    """Convert fuses.json data to nca.txt format."""
    lines = [NCA_HEADER]

    # Sort by version descending (newest first)
    sorted_data = sorted(data, key=lambda x: parse_version_tuple(x['version']), reverse=True)

    # Collect entries
    system_entries = []
    exfat_entries = []

    for entry in sorted_data:
        ver = entry['version']
        system_nca = entry.get('system_title_nca', '')
        exfat_nca = entry.get('exfat_title_nca', '')

        if system_nca:
            system_entries.append(f"[NCA] {ver} {system_nca} {TITLE_ID_SYSTEM_VERSION}")
        if exfat_nca:
            exfat_entries.append(f"[NCA] {ver} {exfat_nca} {TITLE_ID_EXFAT}")

    # Add SystemVersion section
    lines.append("# SystemVersion NCAs (Title ID: 0100000000000809)")
    lines.extend(system_entries)
    lines.append("")

    # Add ExFat section
    lines.append("# ExFat NCAs (Title ID: 010000000000081B - BootImagePackageExFat)")
    lines.extend(exfat_entries)
    lines.append("")

    return "\n".join(lines)


def main():
    """Main function."""
    print("=" * 60)
    print("NxNandManager NCA Database Updater")
    print("=" * 60)

    # Fetch data
    try:
        fuses_data = fetch_fuses_json()
        print(f"Retrieved {len(fuses_data['data'])} firmware versions")
    except Exception as e:
        print(f"Error fetching fuses.json: {e}")
        return 1

    # Convert
    nca_content = convert_to_nca_txt(fuses_data['data'])

    # Write output
    output_path = os.path.normpath(OUTPUT_PATH)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(nca_content)

    print(f"Updated {output_path}")
    print(f"Total entries: {nca_content.count('[NCA]')}")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    exit(main())
