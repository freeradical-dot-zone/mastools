#!/usr/bin/env python

"""
Show any new, changed, or deleted accounts that mention URLs in their account info.

This is super common for spammers, who like to stuff their crummy website's info into every single
field possible. Suppose you run this hourly and email yourself the results (which will usually be
empty unless your instance is *very* busy). Now you can catch those "https://support-foo-corp/"
spammers before they have a chance to post!
"""

import argparse
from operator import itemgetter

from mastools.models import session_for, Accounts
from mastools.scripts import common

CACHE_KEY = "users"
CACHE_VERSION = 1


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


def render_field_changes(old_fields, new_fields):
    """Pretty-print changes in a user's bio fields."""

    if not (old_fields or new_fields):
        yield "  <none>"
        return

    if sorted(old_fields, key=itemgetter("name", "value")) == sorted(
        new_fields, key=itemgetter("name", "value")
    ):
        yield "  <unchanged>"
        return

    old_set = {(field["name"], field["value"]) for field in old_fields}
    new_set = {(field["name"], field["value"]) for field in new_fields}

    for field in sorted(old_set - new_set):
        yield f"  - {field[0]!r}: {field[1]!r}"

    for field in sorted(old_set & new_set):
        yield f"    {field[0]!r}: {field[1]!r}"

    for field in sorted(new_set - old_set):
        yield f"  + {field[0]!r}: {field[1]!r}"


def render_note_changes(old_note, new_note):
    """Pretty-print changes in a user's bio note."""

    if not (old_note or new_note):
        yield "  <none>"
        return

    if old_note == new_note:
        yield "  <unchanged>"
        return

    # Returning the repr (`!r`) protects from email header injection by crafty users. See
    # https://www.thesitewizard.com/php/protect-script-from-email-injection.shtml for an
    # explanation.

    if old_note:
        yield f"  - {old_note!r}"

    if new_note:
        yield f"  + {new_note!r}"


def render_new_user(username, data):
    """Pretty-print information about a new user."""

    yield f"New user: {username}"

    yield " fields:"
    yield from render_field_changes({}, data["fields"])

    yield " note:"
    yield from render_note_changes("", data["note"])


def render_changed_user(username, old_data, new_data):
    """Pretty-print information about a changed user."""

    yield f"Changed user: {username}"

    yield " fields:"
    yield from render_field_changes(old_data["fields"], new_data["fields"])

    yield " note:"
    yield from render_note_changes(old_data["note"], new_data["note"])


def render_deleted_user(username, data):
    """Pretty-print information about a deleted user."""

    yield f"Deleted user: {username}"

    yield " fields:"
    yield from render_field_changes(data["fields"], {})

    yield " note:"
    yield from render_note_changes(data["note"], "")


def show_output(gen):
    """Print each line of output to stdout, then a blank line.

    Building the output this way is a little unusual, but it's much easier to test. Also, adopting
    this convention means that we don't have to build up the output inside each rendering function,
    so they can be as simple as possible and not have to track their own state.
    """

    for line in gen:
        print(line)

    print()


def setup_command_line(subgroup, parent):
    """Add the subcommand."""

    this = subgroup.add_parser(
        "show-user-changes", help=show_user_changes.__doc__, parents=[parent]
    )
    this.set_defaults(func=show_user_changes)


def handle_command_line():
    """Backward-compatible command line setup."""

    parser = argparse.ArgumentParser(description=show_user_changes.__doc__)
    args = parser.parse_args()
    show_user_changes(args)


def show_user_changes(args):  # pylint: disable=unused-argument
    """Fetch all current users with URLs in their account info and show any changes."""

    session = session_for(**common.get_config())

    old_users = common.load_cache(CACHE_KEY, CACHE_VERSION)
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

    common.save_cache(CACHE_KEY, CACHE_VERSION, new_users)
