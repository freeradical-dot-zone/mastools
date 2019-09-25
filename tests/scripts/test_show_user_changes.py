"""Test the show_user_changes script."""

from mastools.scripts import show_user_changes


def collect(gen):
    """Turn the output of a generator into a string we can compare."""

    return "\n".join(list(gen)) + "\n"


def test_render_field_changes():
    """Assert old and new fields are formatted correctly."""

    def make_item(name, value):
        return {"name": name, "value": value}

    old_fields = [
        make_item("one", "A"),
        make_item("two", "B"),
        make_item("two", "C"),
        make_item("three", "D"),
    ]
    new_fields = [
        make_item("uno", "A"),
        make_item("two", "B"),
        make_item("three", "D"),
        make_item("three", "E"),
        make_item("four", "F"),
    ]

    assert (
        collect(show_user_changes.render_field_changes(old_fields, new_fields))
        == """\
  - 'one': 'A'
  - 'two': 'C'
    'three': 'D'
    'two': 'B'
  + 'four': 'F'
  + 'three': 'E'
  + 'uno': 'A'
"""
    )


def test_render_new_user():
    """New users are displayed as expected."""

    out = show_user_changes.render_new_user("newuser", {"fields": [], "note": "I'm new."})

    assert (
        collect(out)
        == """\
New user: newuser
 fields:
 note:
  + "I'm new."
"""
    )


def test_render_changed_user():
    """Changed users are displayed as expected."""

    out = show_user_changes.render_changed_user(
        "activeuser",
        {"fields": [], "note": None},
        {"fields": [{"name": "likes", "value": "puppies, infosec"}], "note": "hack the planet"},
    )

    assert (
        collect(out)
        == """\
Changed user: activeuser
 fields:
  + 'likes': 'puppies, infosec'
 note:
  - <none>
  + 'hack the planet'
"""
    )


def test_render_changed_user_but_not_really():
    """Maaaaybe-changed users are displayed as expected."""

    out = show_user_changes.render_changed_user(
        "activeuser",
        {"fields": [{"name": "likes", "value": "puppies, infosec"}], "note": "hack the planet"},
        {"fields": [{"name": "likes", "value": "puppies, infosec"}], "note": "hack the planet"},
    )

    # We should never be here if neither fields nor note have changed, but let's ignore that for
    # testing. Cut admins a break and tell them up front when a user's field or notes haven't
    # changed.
    assert (
        collect(out)
        == """\
Changed user: activeuser
 fields:
  <unchanged>
 note:
  <unchanged>
"""
    )


def test_render_deleted_user():
    """Deleted users are displayed as expected."""

    out = show_user_changes.render_deleted_user(
        "spammer",
        {
            "fields": [{"name": "support", "value": "https://example.com/send-me-cash"}],
            "note": "I like to\n\n.\n\nFrom: spammer@example.com\nSubject: Inject spam",
        },
    )

    assert (
        collect(out)
        == """\
Deleted user: spammer
 fields:
  - 'support': 'https://example.com/send-me-cash'
 note:
  - 'I like to\\n\\n.\\n\\nFrom: spammer@example.com\\nSubject: Inject spam'
"""
    )
