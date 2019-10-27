"""Model the Accounts table."""

from sqlalchemy import Column, DateTime, Integer, JSON, String, Text

from .base import Base


class Accounts(Base):
    """The Accounts table."""

    # pylint: disable=too-few-public-methods  ; We know.

    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    domain = Column(String)
    created_at = Column(DateTime, nullable=False)
    note = Column(Text, nullable=False)
    fields = Column(JSON)
    suspended_at = Column(DateTime)


# pylint: disable=line-too-long  ; copied-and-pasted from PostgreSQL

# Note: columns are added as-needed. If we get overly ambitious and add everything at once, this is
# more likely to drift out of date with the upstream Mastodon table definitions.

# As of 2019-09-24, upstream defines these columns:

# *username                | character varying           |           | not null | ''::character varying
# *domain                  | character varying           |           |          |
#  secret                  | character varying           |           | not null | ''::character varying
#  private_key             | text                        |           |          |
#  public_key              | text                        |           | not null | ''::text
#  remote_url              | character varying           |           | not null | ''::character varying
#  salmon_url              | character varying           |           | not null | ''::character varying
#  hub_url                 | character varying           |           | not null | ''::character varying
# *created_at              | timestamp without time zone |           | not null |
#  updated_at              | timestamp without time zone |           | not null |
# *note                    | text                        |           | not null | ''::text
#  display_name            | character varying           |           | not null | ''::character varying
#  uri                     | character varying           |           | not null | ''::character varying
#  url                     | character varying           |           |          |
#  avatar_file_name        | character varying           |           |          |
#  avatar_content_type     | character varying           |           |          |
#  avatar_file_size        | integer                     |           |          |
#  avatar_updated_at       | timestamp without time zone |           |          |
#  header_file_name        | character varying           |           |          |
#  header_content_type     | character varying           |           |          |
#  header_file_size        | integer                     |           |          |
#  header_updated_at       | timestamp without time zone |           |          |
#  avatar_remote_url       | character varying           |           |          |
#  subscription_expires_at | timestamp without time zone |           |          |
#  locked                  | boolean                     |           | not null | false
#  header_remote_url       | character varying           |           | not null | ''::character varying
#  last_webfingered_at     | timestamp without time zone |           |          |
#  inbox_url               | character varying           |           | not null | ''::character varying
#  outbox_url              | character varying           |           | not null | ''::character varying
#  shared_inbox_url        | character varying           |           | not null | ''::character varying
#  followers_url           | character varying           |           | not null | ''::character varying
#  protocol                | integer                     |           | not null | 0
#  id                      | bigint                      |           | not null | nextval('accounts_id_seq'::regclass)
#  memorial                | boolean                     |           | not null | false
#  moved_to_account_id     | bigint                      |           |          |
#  featured_collection_url | character varying           |           |          |
# *fields                  | jsonb                       |           |          |
#  actor_type              | character varying           |           |          |
#  discoverable            | boolean                     |           |          |
#  also_known_as           | character varying[]         |           |          |
#  silenced_at             | timestamp without time zone |           |          |
# *suspended_at            | timestamp without time zone |           |          |
