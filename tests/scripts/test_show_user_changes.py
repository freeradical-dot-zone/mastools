"""Test the show_user_changes script."""

from mastools.scripts import show_user_changes


def collect(gen):
    """Turn the output of a generator into a string we can compare."""

    return "\n".join(list(gen))


def test_render_new_user():
    """New users are displayed as expected."""

    out = show_user_changes.render_new_user("newuser", {"fields": [], "note": "I'm new."})

    assert (
        collect(out)
        == """\
New user: newuser
+ fields: []
+ note: I'm new."""
    )


def test_render_changed_user():
    """Changed users are displayed as expected."""

    out = show_user_changes.render_changed_user(
        "activeuser",
        {"fields": [], "note": "i just got here"},
        {"fields": [{"name": "likes", "value": "puppies, infosec"}], "note": "hack the planet"},
    )

    assert (
        collect(out)
        == """\
Changed user: activeuser
- fields: []
+ fields: [{'name': 'likes', 'value': 'puppies, infosec'}]
- mote: i just got here
+ note: hack the planet"""
    )


def test_render_deleted_user():
    """Deleted users are displayed as expected."""

    out = show_user_changes.render_deleted_user(
        "spammer",
        {
            "fields": [{"name": "support", "value": "https://example.com/send-me-cash"}],
            "note": "Send me your money!",
        },
    )

    assert (
        collect(out)
        == """\
Deleted user: spammer
- fields: [{'name': 'support', 'value': 'https://example.com/send-me-cash'}]
- note: Send me your money!"""
    )
