#!/usr/bin/env python

"""
Show any new, changed, or deleted accounts that mention URLs in their account info.

This is super common for spammers, who like to stuff their crummy website's info into every single
field possible. Suppose you run this hourly and email yourself the results (which will usually be
empty unless your instance is *very* busy). Now you can catch those "https://support-foo-corp/"
spammers before they have a chance to post!
"""

import argparse
import json
from pathlib import Path

from mastools.models import session_for, Accounts

CACHE_FILE = "~/.mastools/usercache.json"
CONFIG_FILE = "~/.mastools/config.json"


def has_url(account: Accounts) -> str:
    """Return True if the account's note or fields seem to contain a URL."""

    if account.note and "http" in account.note.lower():
        return True
    if "http" in str(account.fields).lower():
        return True
    return False


def users_with_urls(session):
    """Return a dictionary of usernames to their account info when they mention URLs."""

    query = (
        session.query(Accounts)
        .filter(Accounts.domain == None)  # pylint: disable=singleton-comparison
        .filter(Accounts.suspended_at == None)  # pylint: disable=singleton-comparison
        .order_by(Accounts.created_at)
    )

    return {
        account.username: {"fields": account.fields, "note": account.note}
        for account in query
        if has_url(account)
    }


def handle_command_line():
    """Fetch all changed current users with URLs in their account info and show any changes."""

    parser = argparse.ArgumentParser(description=handle_command_line.__doc__)
    parser.parse_args()

    cache_file = Path(CACHE_FILE).expanduser()
    config_file = Path(CONFIG_FILE).expanduser()

    config = json.loads(config_file.read_text())
    session = session_for(**config)

    # Try to get the results of the last run, but fall back to an empty dict if that's not
    # available. That's most likely to happen on the first run.
    try:
        old_users = json.loads(cache_file.read_text())["users"]
    except FileNotFoundError:
        old_users = {}

    new_users = users_with_urls(session)

    for username, new_data in new_users.items():
        try:
            old_data = old_users.pop(username)
        except KeyError:
            # If the username isn't in the old data, then they're new. Report than and move on to
            # the next account.
            print("New user:", username)
            print("Fields:", new_data["fields"])
            print("Note:", new_data["note"])
            print("-" * 30)
            continue

        if old_data == new_data:
            continue

        # Something's changed since the last time we saw this user. Report that.
        print("Changed user:", username)
        print("Old Fields:", old_data["fields"])
        print("Old Note:", old_data["note"])
        print("New Fields:", new_data["fields"])
        print("New Note:", new_data["note"])
        print("-" * 30)

    # Report any leftover old accounts that aren't in the new accounts. They were probably
    # suspended.
    for username, old_data in old_users.items():
        print("Deleted user:", username)
        print("Old Fields:", old_data["fields"])
        print("Old Note:", old_data["note"])
        print("-" * 30)

    # Save these results for the next run. Include the version information and nest the user
    # information inside a "users" key from the start, because experience says if we don't do this
    # then the next release will add a feature that requires a change in the data layout, and then
    # we'll have to write a data migration or something.
    cache_file.write_text(json.dumps({"users": new_users, "version": 1}))
