"""Show users who haven't confirmed their email yet."""

import logging

from mastools.models import session_for, Users
from mastools.scripts import common

LOG = logging.getLogger(__name__)


def setup_command_line(subgroup, parent):
    """Add the subcommand."""

    this = subgroup.add_parser(
        "show-unconfirmed-users", help=show_unconfirmed_users.__doc__, parents=[parent]
    )
    this.set_defaults(func=show_unconfirmed_users)


def show_unconfirmed_users(args):  # pylint: disable=unused-argument
    """Show users who haven't confirmed their email yet."""

    session = session_for(**common.get_config())

    LOG.debug("fetching unconfirmed accounts")

    query = (
        session.query(Users)
        .filter(Users.confirmed_at == None)  # pylint: disable=singleton-comparison
        .order_by(Users.created_at)
    )

    for user in query:
        print(f"{user.account.username} <{user.email}> was created at {user.created_at}")

    LOG.info("found %d unconfirmed accounts", query.count())
