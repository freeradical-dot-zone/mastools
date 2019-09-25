"""Common things used by all scripts."""

import json
from pathlib import Path

MASTOOLS_DIR = Path("~/.mastools").expanduser()
CONFIG_FILE = MASTOOLS_DIR / "config.json"


def get_config():
    """Return the parsed contents of the config file."""

    return json.loads(CONFIG_FILE.read_text())


def cache_file(cache_key):
    """Return the Path of the cache file for the key."""

    return MASTOOLS_DIR / f"{cache_key}_cache.json"


def load_cache(cache_key, version):
    """Return the contents of the cache for the key, if its version is correct."""

    # Try to get the results of the last run, but fall back to an empty dict if that's not
    # available. That's most likely to happen on the first run.
    try:
        cache = json.loads(cache_file(cache_key).read_text())
    except FileNotFoundError:
        return {}

    if cache["version"] != version:
        raise ValueError(
            f"Unknown {cache_key} version number: expected {version}, got {cache['version']}"
        )

    return cache[cache_key]


def save_cache(cache_key, version, data):
    """Write the data to the cache for the key."""

    # Save these results for the next run. Include the version information and nest the user
    # information inside a "users" key from the start, because experience says if we don't do this
    # then the next release will add a feature that requires a change in the data layout, and then
    # we'll have to write a data migration or something.

    cache_data = {cache_key: data, "version": version}

    cache_file(cache_key).write_text(json.dumps(cache_data, indent=2))
