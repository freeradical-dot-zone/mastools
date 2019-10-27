"""Configure the mastools command."""

import argparse

from . import unconfirmed_users, user_changes


def handle_command_line():
    """Create a command command line, then parse it."""

    parser = argparse.ArgumentParser(description=handle_command_line.__doc__)

    children = parser.add_subparsers(
        title="Subcommands", description="Valid subcommands", help="Subcommand details"
    )

    for child_module in (unconfirmed_users, user_changes):
        child_module.setup_command_line(children)

    args = parser.parse_args()
    try:
        func = args.func
    except AttributeError:
        parser.print_help()
        return
    func(args)
