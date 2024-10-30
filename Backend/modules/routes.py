""" Routes file. """
from flask import request, jsonify, Blueprint
from flask.wrappers import Response
from flask_login import login_user, logout_user, login_required

from . import db
from .models import Accounts, Clients, Employee


routes = Blueprint("routes", __name__)


@routes.route("/register", methods=["POST"])
def register() -> tuple[Response, int]:
  """ User register endpoint. """
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
    print("Creating client account.")
    firstname = data.get("firstname")
    lastname = data.get("lastname")
    telephone = data.get("telephone")
    client = Clients(account_id=user.account_id, firstname=firstname,
                     lastname=lastname, telephone=telephone)
    db.session.add(client)
    db.session.commit()
  elif role == "employee":
    print("Creating employee account.")
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

  return jsonify({"message": "User registered successfully!"}), 201


@routes.route("/login", methods=["POST"])
def login() -> tuple[Response, int]:
  """ User login endpoint. """
  data = request.get_json()
  email = data.get("email")
  password = data.get("password")

  user = Accounts.query.filter_by(email=email).first()
  if user and user.password == password:
    login_user(user)
    return jsonify({"message": "Logged in successfully!"}), 200
  else:
    return jsonify({"message": "Login failed! Check email and password."}), 401


@routes.route("/login_check", methods=["GET"])
@login_required
def login_check() -> tuple[Response, int]:
  """ Endpoint used in development for checking if user is logged in. """
  return jsonify({"message": "User is logged in!"}), 200


@routes.route("/logout", methods=["POST"])
@login_required
def logout() -> tuple[Response, int]:
  """ User logout endpoint. """
  logout_user()
  return jsonify({"message": "User logged out successfully!"}), 200
