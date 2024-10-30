""" Models file. """
from flask_login import UserMixin

from . import db


class Accounts(db.Model, UserMixin):
  """ Accounts table configuration. """
  account_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(50), nullable=False)
  role = db.Column(db.String(50), nullable=False)

  def __repr__(self) -> str:
    """ Returns user email. """
    return f"User('{self.email}')"

  def get_id(self) -> int:
    """ Returns account id. """
    return self.account_id
