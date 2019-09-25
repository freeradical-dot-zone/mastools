"""Test the show_user_changes script."""

from mastools.scripts import show_user_changes


def test_render_new_user(capsys):
    """New users are displayed as expected."""

    show_user_changes.render_new_user("newuser", {"fields": [], "note": "I'm new."})

    captured = capsys.readouterr()
    assert (
        captured.out
        == """\
New user: newuser
+ fields: []
+ note: I'm new.

"""
    )


def test_render_changed_user(capsys):
    """Changed users are displayed as expected."""

    show_user_changes.render_changed_user(
        "activeuser",
        {"fields": [], "note": "i just got here"},
        {"fields": [{"name": "likes", "value": "puppies, infosec"}], "note": "hack the planet"},
    )

    captured = capsys.readouterr()
    assert (
        captured.out
        == """\
Changed user: activeuser
- fields: []
+ fields: [{'name': 'likes', 'value': 'puppies, infosec'}]
- mote: i just got here
+ note: hack the planet

"""
    )


def test_render_deleted_user(capsys):
    """Deleted users are displayed as expected."""

    show_user_changes.render_deleted_user(
        "spammer",
        {
            "fields": [{"name": "support", "value": "https://example.com/send-me-cash"}],
            "note": "Send me your money!",
        },
    )

    captured = capsys.readouterr()
    assert (
        captured.out
        == """\
Deleted user: spammer
- fields: [{'name': 'support', 'value': 'https://example.com/send-me-cash'}]
- note: Send me your money!

"""
    )
