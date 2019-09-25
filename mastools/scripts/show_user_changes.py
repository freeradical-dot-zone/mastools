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
from operator import itemgetter
from pathlib import Path

from mastools.models import session_for, Accounts

CACHE_FILE = "~/.mastools/usercache.json"
CONFIG_FILE = "~/.mastools/config.json"


def has_url(account: Accounts) -> bool:
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


def render_fields(prefix, fields):
    """Pretty-print a user's bio fields."""

    if not fields:
        yield f"  {prefix} <none>"
        return

    for field in sorted(fields, key=itemgetter("name")):
        yield f"  {prefix} {field['name']!r}: {field['value']!r}"


def render_note(prefix, note):
    """Pretty-print a user's bio note."""

    if not note:
        yield f"  {prefix} <none>"
        return

    # This protects from email header injection from crafty users. See
    # https://www.thesitewizard.com/php/protect-script-from-email-injection.shtml for an
    # explanation.
    yield f"  {prefix} {note!r}"


def render_new_user(username, data):
    """Pretty-print information about a new user."""

    yield f"New user: {username}"

    yield " fields:"
    yield from render_fields("+", data["fields"])

    yield " note:"
    yield from render_note("+", data["note"])


def render_changed_user(username, old_data, new_data):
    """Pretty-print information about a changed user."""

    yield f"Changed user: {username}"

    yield " fields:"
    if old_data["fields"] == new_data["fields"]:
        yield "  <unchanged>"
    else:
        yield from render_fields("-", old_data["fields"])
        yield from render_fields("+", new_data["fields"])

    yield " note:"
    if old_data["note"] == new_data["note"]:
        yield "  <unchanged>"
    else:
        yield from render_note("-", old_data["note"])
        yield from render_note("+", new_data["note"])


def render_deleted_user(username, data):
    """Pretty-print information about a deleted user."""

    yield f"Deleted user: {username}"

    yield " fields:"
    yield from render_fields("-", data["fields"])

    yield " note:"
    yield from render_note("-", data["note"])


def show_output(gen):
    """Print each line of output to stdout, then a blank line.

    Building the output this way is a little unusual, but it's much easier to test. Also, adopting
    this convention means that we don't have to build up the output inside each rendering function,
    so they can be as simple as possible and not have to track their own state.
    """

    for line in gen:
        print(line)

    print()


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
            show_output(render_new_user(username, new_data))
            continue

        if old_data != new_data:
            # Something's changed since the last time we saw this user. Report that.
            show_output(render_changed_user(username, old_data, new_data))

    # Report any leftover old accounts that aren't in the new accounts. They were probably
    # suspended.
    for username, old_data in old_users.items():
        show_output(render_deleted_user(username, old_data))

    # Save these results for the next run. Include the version information and nest the user
    # information inside a "users" key from the start, because experience says if we don't do this
    # then the next release will add a feature that requires a change in the data layout, and then
    # we'll have to write a data migration or something.
    cache_file.write_text(json.dumps({"users": new_users, "version": 1}))
