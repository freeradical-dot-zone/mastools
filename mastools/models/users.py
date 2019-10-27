"""Model the Users table."""

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base


class Users(Base):
    """The Users table."""

    # pylint: disable=too-few-public-methods  ; We know.

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    confirmed_at = Column(DateTime)
    account_id = Column(ForeignKey("accounts.id"), nullable=False)

    account = relationship("Accounts")


# pylint: disable=line-too-long  ; copied-and-pasted from PostgreSQL

# Note: columns are added as-needed. If we get overly ambitious and add everything at once, this is
# more likely to drift out of date with the upstream Mastodon table definitions.

# As of 2019-10-27, upstream defines these columns:

#  email                     | character varying           |           | not null | ''::character varying
#  created_at                | timestamp without time zone |           | not null |
#  updated_at                | timestamp without time zone |           | not null |
#  encrypted_password        | character varying           |           | not null | ''::character varying
#  reset_password_token      | character varying           |           |          |
#  reset_password_sent_at    | timestamp without time zone |           |          |
#  remember_created_at       | timestamp without time zone |           |          |
#  sign_in_count             | integer                     |           | not null | 0
#  current_sign_in_at        | timestamp without time zone |           |          |
#  last_sign_in_at           | timestamp without time zone |           |          |
#  current_sign_in_ip        | inet                        |           |          |
#  last_sign_in_ip           | inet                        |           |          |
#  admin                     | boolean                     |           | not null | false
#  confirmation_token        | character varying           |           |          |
#  confirmed_at              | timestamp without time zone |           |          |
#  confirmation_sent_at      | timestamp without time zone |           |          |
#  unconfirmed_email         | character varying           |           |          |
#  locale                    | character varying           |           |          |
#  encrypted_otp_secret      | character varying           |           |          |
#  encrypted_otp_secret_iv   | character varying           |           |          |
#  encrypted_otp_secret_salt | character varying           |           |          |
#  consumed_timestep         | integer                     |           |          |
#  otp_required_for_login    | boolean                     |           | not null | false
#  last_emailed_at           | timestamp without time zone |           |          |
#  otp_backup_codes          | character varying[]         |           |          |
#  filtered_languages        | character varying[]         |           | not null | '{}'::character varying[]
#  account_id                | bigint                      |           | not null |
#  id                        | bigint                      |           | not null | nextval('users_id_seq'::regclass)
#  disabled                  | boolean                     |           | not null | false
#  moderator                 | boolean                     |           | not null | false
#  invite_id                 | bigint                      |           |          |
#  remember_token            | character varying           |           |          |
#  chosen_languages          | character varying[]         |           |          |
#  created_by_application_id | bigint                      |           |          |
#  approved                  | boolean                     |           | not null | true
# Indexes:
#     "index_users_on_id" PRIMARY KEY, btree (id)
#     "index_users_on_confirmation_token" UNIQUE, btree (confirmation_token)
#     "index_users_on_email" UNIQUE, btree (email)
#     "index_users_on_remember_token" UNIQUE, btree (remember_token)
#     "index_users_on_reset_password_token" UNIQUE, btree (reset_password_token)
#     "index_users_on_account_id" btree (account_id)
#     "index_users_on_created_by_application_id" btree (created_by_application_id)
# Foreign-key constraints:
#     "fk_50500f500d" FOREIGN KEY (account_id) REFERENCES accounts(id) ON DELETE CASCADE
#     "fk_rails_8fb2a43e88" FOREIGN KEY (invite_id) REFERENCES invites(id) ON DELETE SET NULL
#     "fk_rails_ecc9536e7c" FOREIGN KEY (created_by_application_id) REFERENCES oauth_applications(id) ON DELETE SET NULL
