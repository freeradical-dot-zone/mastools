"""Test the user_changes script."""

from mastools.scripts import user_changes


def collect(gen):
    """Turn the output of a generator into a string we can compare."""

    return "\n".join(list(gen)) + "\n"


def make_field(name, value):
    """Return a Mastodon-style dict of the name and value."""

    return {"name": name, "value": value}


def make_fields(fields):
    """Return a list of Mastodon-style dicts of the (name, value) fields."""

    return [make_field(*field) for field in fields]


def test_render_field_changes():
    """Changes from old to new fields look kind of like a diff."""

    old_fields = make_fields([("one", "A"), ("two", "B"), ("two", "C"), ("three", "D")])
    new_fields = make_fields(
        [("uno", "A"), ("two", "B"), ("three", "D"), ("three", "E"), ("four", "F")]
    )

    assert (
        collect(user_changes.render_field_changes(old_fields, new_fields))
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


def test_render_field_changes_empty():
    """'Changes to empty fields should say *something*."""

    assert collect(user_changes.render_field_changes({}, {})) == "  <none>\n"


def test_render_field_changes_same():
    """'Changes to unchanged fields should just report that."""

    assert (
        collect(
            user_changes.render_field_changes(
                make_fields([("foo", "bar"), ("spam", "eggs")]),
                make_fields([("foo", "bar"), ("spam", "eggs")]),
            )
        )
        == "  <unchanged>\n"
    )


def test_render_note_changes():
    """Changing a note's contents shows the old and new items."""

    assert (
        collect(user_changes.render_note_changes("old", "new"))
        == """\
  - 'old'
  + 'new'
"""
    )


def test_render_note_changes_became_empty():
    """Deleting an existing note shows only the old value."""

    assert (
        collect(user_changes.render_note_changes("old", ""))
        == """\
  - 'old'
"""
    )


def test_render_note_changes_became_full():
    """Adding a new note shows only the new value."""

    assert (
        collect(user_changes.render_note_changes("", "new"))
        == """\
  + 'new'
"""
    )


def test_render_note_changes_empty():
    """Showing empty note changes highlights that there's nothing there."""

    assert collect(user_changes.render_note_changes("", "")) == "  <none>\n"


def test_render_note_changes_same():
    """Showing existing notes that don't change highlights that they haven't changed."""

    assert collect(user_changes.render_note_changes("Note.", "Note.")) == "  <unchanged>\n"


def test_render_new_user():
    """New users are displayed as expected."""

    out = user_changes.render_new_user("newuser", {"fields": [], "note": "I'm new."})

    assert (
        collect(out)
        == """\
New user: newuser
 fields:
  <none>
 note:
  + "I'm new."
"""
    )


def test_render_changed_user():
    """Changed users are displayed as expected."""

    out = user_changes.render_changed_user(
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
  + 'hack the planet'
"""
    )


def test_render_changed_user_but_not_really():
    """Maaaaybe-changed users are displayed as expected."""

    out = user_changes.render_changed_user(
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

    out = user_changes.render_deleted_user(
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
