#!/usr/bin/env python
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "ruamel-yaml",
# ]
# ///

"""Fix locale files which have been damaged upstream."""

import argparse
import json
from pathlib import Path
from sys import stdout

from ruamel.yaml import YAML


def repair_string(value: str) -> str:
    """Fix a broken locale string."""
    return value.replace("post", "toot").replace("Post", "Toot")


def deep_update(item):
    """Fix arbitrarily deeply nested locale values."""
    for key, value in item.items():
        if isinstance(value, dict):
            deep_update(value)
        else:
            item[key] = repair_string(value)


def repair_json(filepath: Path, overwrite: bool = False):
    """Fix broken strings in JSON files."""
    locale = json.load(filepath.open())
    new_locale = {key: repair_string(value) for key, value in locale.items()}
    output = json.dumps(new_locale, indent=2, ensure_ascii=False)
    if overwrite:
        filepath.write_text(output)
    else:
        stdout.write(output)


def repair_yaml(filepath: Path, overwrite: bool = False):
    """Fix broken strings in YAML files."""
    yaml = YAML()
    yaml.explicit_start = True
    yaml.preserve_quotes = True
    locale = yaml.load(filepath)

    deep_update(locale)

    yaml.width = 10000
    yaml.dump(locale, filepath if overwrite else stdout)


def handle_command_line():
    """Handle the command line."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-w",
        "--overwrite",
        action="store_true",
        help="Write the changes back to the input file.",
    )
    parser.add_argument("filename", type=Path, help="The file to fix.")
    args = parser.parse_args()
    if args.filename.suffix in (".yaml", ".yml"):
        repair_yaml(args.filename, args.overwrite)
    elif args.filename.suffix == ".json":
        repair_json(args.filename, args.overwrite)
    else:
        raise ValueError(f"Unexpected extension: {args.filename.suffix=}")


if __name__ == "__main__":
    handle_command_line()
