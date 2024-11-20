""" API POST functions. """
from flask import request, jsonify, abort
from flask.wrappers import Response
from flask_login import login_user, logout_user, current_user

from . import db
from .models import (
  Accounts, Clients, Employee, Categories
)


def register_user() -> tuple[Response, int]:
  """ Inserts new user to the database. """
  data = request.get_json()
  email = data.get("email")
  password = data.get("password")
  role = data.get("role")

  if Accounts.query.filter_by(email=email).first():
    return jsonify({"message": "Email is already in use!"}), 400

  user = Accounts(email=email, password=password, role=role)
  db.session.add(user)
  db.session.commit()

  if role == "client":
    register_client_account(data, user)
  elif role == "employee":
    register_employee_account(data, user)


def register_client_account(data: dict, user: Accounts) -> None:
  """ Registers client account. """
  firstname = data.get("firstname")
  lastname = data.get("lastname")
  telephone = data.get("telephone")
  client = Clients(account_id=user.account_id, firstname=firstname,
                   lastname=lastname, telephone=telephone)
  db.session.add(client)
  db.session.commit()


def register_employee_account(data: dict, user: Accounts) -> None:
  """ Registers employee account. """
  firstname = data.get("firstname")
  lastname = data.get("lastname")
  telephone = data.get("telephone")
  position = data.get("position")
  is_available = data.get("is_available")
  employee = Employee(account_id=user.account_id, firstname=firstname,
                      lastname=lastname, telephone=telephone,
                      position=position, is_available=is_available)
  db.session.add(employee)
  db.session.commit()


def log_in_user() -> [str, int]:
  """ Logins user. """
  data = request.get_json()
  email = data.get("email")
  password = data.get("password")
  user = Accounts.query.filter_by(email=email).first()
  if user and user.password == password:
    login_user(user)
    return "Logged in successfully!", 200
  else:
    return "Login failed! Check email and password.", 401


def log_out_user() -> [str, int]:
  """ Logs out user. """
  logout_user()
  return "User logged out successfully!", 200


def add_new_category() -> [str, int]:
  """ Inserts new category to the database. """
  if not current_user.is_authenticated:
    abort(401)
  if current_user.role != "admin":
    abort(403)
  data = request.get_json()
  name = data.get("name")
  category = Categories(name=name)
  db.session.add(category)
  db.session.commit()
  return "Successfully added new category", 201
