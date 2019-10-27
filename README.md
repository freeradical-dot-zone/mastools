# mastools - Tools for interacting directly with a Mastodon instance's database

## Installation

If you just want to use mastools and not work on the project itself: `pip install mastools`.

If you want to help develop mastools and have [poetry](https://poetry.eustace.io) installed, clone this repo and run `poetry install`.

If you want to develop mastools but don't have poetry, use `pip` to install the dependencies mentioned in the `[tool.poetry.dependencies]` section of `pyproject.toml`.

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

# The tool

Starting with version 0.2.0, there's only one main `mastools` command which has
multiple subcommands. `show-user-changes` is still a functioning command for
temporary backward compatibility, but it will be removed soon.

`mastools` subcommands:

## show-unconfirmed-users

Show users who haven't confirmed their email yet, ordered by their creation date
from oldest to newest.

This is useful for detection a flood of newly created junk accounts.

```
$ mastools show-unconfired-users
crqcrujofa <cfvzm@example.com> was created at 2019-10-25 10:10:18.406158
lkjmadf <ljchrew@example.com> was created at 2019-10-25 13:06:04.175580
```

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
10 * * * * /home/me/mastools/.venv/bin/mastools show-user-changes
```

to get an hourly update of changes. This gives a report like:

```
Changed user: tek
 fields:
  - 'Avatar': 'Me, at night, with tunes'
    'Website': 'https://honeypot.net'
  + 'Avatar': 'Me, at night, with music'
 note:
  <unchanged>

New user: new_spammer
 fields:
  + 'website': 'https://example.com/foo-corp-tech-support'
 note:
  + 'ALL UR FRAUD^WSUPPORT NEEDS'

Deleted user: old_spammer
 fields:
  - 'website': 'https://example.com/bar-inc-tech-support'
 note:
  - 'SEND ME YOUR IP ADDRESS AND CREDIT CARD'
```

# License

Distributed under the terms of the MIT license, mastools is free and open source software.

# History

- v0.2.0 - 2019-10-27: Added `mastools` command and `show_unconfirmed_users` subcommand
- v0.1.3 - 2019-09-25: Productionizing
- v0.1.2 - 2019-09-25: Prettier show-user-changes output
- v0.1.1 - 2019-09-24: Same code, but pushing new metadata to pypi
- v0.1.0 - 2019-09-24: First release
