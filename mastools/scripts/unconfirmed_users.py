"""Show users who haven't confirmed their email yet."""

from mastools.models import session_for, Users
from mastools.scripts import common


def setup_command_line(children):
    """Add the subcommand."""

    this = children.add_parser("show_unconfirmed_users", help=show_unconfirmed_users.__doc__)
    this.set_defaults(func=show_unconfirmed_users)


def show_unconfirmed_users(args):
    """Show users who haven't confirmed their email yet."""

    session = session_for(**common.get_config())

    query = (
        session.query(Users)
        .filter(Users.confirmed_at == None)  # pylint: disable=singleton-comparison
        .order_by(Users.created_at)
    )

    for user in query:
        print(f"{user.account.username} <{user.email}>")
