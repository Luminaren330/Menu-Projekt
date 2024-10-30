""" Models file. """
from flask_login import UserMixin

from . import db


class Accounts(db.Model, UserMixin):
  """ Accounts table configuration. """
  account_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(50), nullable=False)
  role = db.Column(db.String(50), nullable=False)

  def __init__(self, email: str, password: str, role: str) -> None:
    """ Class constructor """
    self.email = email
    self.password = password
    self.role = role

  def __repr__(self) -> str:
    """ Returns user email. """
    return f"User('{self.email}')"

  def get_id(self) -> int:
    """ Returns account id. """
    return self.account_id


class Clients(db.Model, UserMixin):
  """ Clients table configuration. """
  client_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  account_id = db.Column(db.Integer, db.ForeignKey("accounts.account_id"),
                         nullable=False)
  firstname = db.Column(db.String(70), nullable=False)
  lastname = db.Column(db.String(150), nullable=False)
  telephone = db.Column(db.String(15), nullable=False)

  account = db.relationship("Accounts", backref="clients", lazy=True)

  def __init__(
    self, account_id: int, firstname: str, lastname: str, telephone: str
  ) -> None:
    """ Class constructor """
    self.account_id = account_id
    self.firstname = firstname
    self.lastname = lastname
    self.telephone = telephone

  def __repr__(self) -> str:
    """ Returns user first name and last name. """
    return f"Client('{self.firstname}', '{self.lastname}')"

  def get_id(self) -> int:
    """ Returns client id. """
    return self.client_id


class Employee(db.Model, UserMixin):
  """ Employee table configuration. """
  employee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  account_id = db.Column(db.Integer, db.ForeignKey("accounts.account_id"),
                         nullable=False)
  firstname = db.Column(db.String(70), nullable=False)
  lastname = db.Column(db.String(150), nullable=False)
  telephone = db.Column(db.String(15), nullable=False)
  position = db.Column(db.String(40), nullable=False)
  is_available = db.Column(db.Boolean, default=True, nullable=False)

  account = db.relationship("Accounts", backref="employee", lazy=True)

  def __init__(
      self, account_id: int, firstname: str, lastname: str, telephone: str,
      position: str, is_available: bool
  ) -> None:
    """ Class constructor """
    self.account_id = account_id
    self.firstname = firstname
    self.lastname = lastname
    self.telephone = telephone
    self.position = position
    self.is_available = is_available

  def __repr__(self) -> str:
    """ Returns user first name and last name. """
    return f"Employee('{self.firstname}', '{self.lastname}')"

  def get_id(self) -> int:
    """ Returns employee id. """
    return self.employee_id
