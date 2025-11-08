"""Configure the mastools command."""

import argparse
import logging

from . import unconfirmed_users, user_changes


def handle_command_line():
    """Create a command command line, then parse it."""

    parser = argparse.ArgumentParser(description=handle_command_line.__doc__)

    subgroup = parser.add_subparsers(
        title="Subcommands", description="Valid subcommands", help="Subcommand details"
    )

    universal = argparse.ArgumentParser(add_help=False)
    universal.add_argument(
        "--verbose", "-v", help="Increase logging verbosity", action="count", default=0
    )

    for child_module in (unconfirmed_users, user_changes):
        child_module.setup_command_line(subgroup, universal)

    args = parser.parse_args()
    try:
        func = args.func
    except AttributeError:
        parser.print_help()
        return

    # Use the same verbosity settings everywhere
    log_level = logging.WARNING
    if args.verbose == 1:
        log_level = logging.INFO
    if args.verbose >= 2:
        log_level = logging.DEBUG

    logging.basicConfig(level=log_level)

    func(args)
