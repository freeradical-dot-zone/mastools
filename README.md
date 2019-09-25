# mastools - Tools for interacting directly with a Mastodon instance's database

## Installation

If you just want to use mastools and not work on the project itself: `pip install mastools`.

If you have [poetry](https://poetry.eustace.io) installed, run `poetry install`.

If not, use `pip` to install the dependencies mentioned in the `[tool.poetry.dependencies]` section of `pyproject.toml`.

## Configuration

Make a file named `~/.mastools/config.json` like:

```json
{
    "host": "localhost",
    "database": "mastodon",
    "user": "mastodon",
    "password": "0xdeadbeef"
}
```

All mastools components will use this database configuration.

# The tools

## show-user-changes

Show any new, changed, or deleted accounts that mention URLs in their account
info.

This is super common for spammers, who like to stuff their crummy website's info
into every single field possible. Suppose you run this hourly and email yourself
the results (which will usually be empty unless your instance is *very* busy).
Now you can catch those "https://support-foo-corp/" spammers before they have a
chance to post!

For example I run this from a cron job on my instance like:

```
10 * * * * /home/me/mastools/.venv/bin/show-user-changes
```

to get an hourly update of changes.

# License

Distributed under the terms of the `MIT`_ license, mastrools is free and open source software.

# History

- v0.1.2 - 2019-09-25: Prettier show-user-changes output
- v0.1.1 - 2019-09-24: Same code, but pushing new metadata to pypi
- v0.1.0 - 2019-09-24: First release
