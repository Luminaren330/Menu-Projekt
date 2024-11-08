""" Routes file. """
from flask import request, jsonify, Blueprint, abort
from flask.wrappers import Response
from flask_login import login_user, logout_user, login_required, current_user

from . import db
from .models import Accounts, Clients, Employee, Categories, Ingredients


routes = Blueprint("routes", __name__)


@routes.route("/register", methods=["POST"])
def register() -> tuple[Response, int]:
  """
  User register endpoint.
  To register client account pass to the endpoint body following data:
  email, password, role="client", firstname, lastname, telephone.
  To register employee account pass to the endpoint body following data:
  email, password, role="employee", firstname, lastname, telephone, position,
  is_available.
  To register admin account pass to the endpoint body following data:
  email, password, role="admin".
  """
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
  """
  User login endpoint.
  To login user pass to the endpoint body following data: email, password.
  """
  data = request.get_json()
  email = data.get("email")
  password = data.get("password")

  user = Accounts.query.filter_by(email=email).first()
  if user and user.password == password:
    login_user(user)
    return jsonify({"message": "Logged in successfully!"}), 200
  else:
    return jsonify({"message": "Login failed! Check email and password."}), 401


@routes.route("/logout", methods=["POST"])
@login_required
def logout() -> tuple[Response, int]:
  """ User logout endpoint. """
  logout_user()
  return jsonify({"message": "User logged out successfully!"}), 200


@routes.route("/categories", methods=["GET", "POST"])
def manage_categories() -> tuple[Response, int]:
  """
  Endpoint used to manage categories.
  To add new category use POST method. Pass the following data to the endpoint
  body: name.
  ONLY admin user can add new categories.
  To retrieve all categories from table use GET method. Unauthorized users
  can retrieve this data.
  """
  if request.method == "GET":
    categories = Categories.query.with_entities(Categories.name).all()
    response = {"count": len(categories), "records": []}
    categories_to_return = [{"name": category.name} for category in categories]
    response["records"] = categories_to_return
    return jsonify(response), 200
  elif request.method == "POST":
    if not current_user.is_authenticated:
      abort(401)
    if current_user.role != "admin":
      abort(403)
    data = request.get_json()
    name = data.get("name")
    category = Categories(name=name)
    db.session.add(category)
    db.session.commit()
    return jsonify({"message": "Successfully added new category!"}), 201


@routes.route("/ingredients", methods=["GET", "POST"])
def manage_ingredients() -> tuple[Response, int]:
  """
  Endpoint used to manage ingredients.
  To add new ingredient use POST method. Pass the following data to the endpoint
  body: name.
  ONLY admin user can add new ingredients.
  To retrieve all ingredients from table use GET method. Unauthorized users
  can retrieve this data.
  """
  if request.method == "GET":
    ingredients = Ingredients.query.with_entities(Ingredients.name).all()
    response = {"count": len(ingredients), "records": []}
    ingredients_to_return = [
      {"name": ingredient.name} for ingredient in ingredients]
    response["records"] = ingredients_to_return
    return jsonify(response), 200
  elif request.method == "POST":
    if not current_user.is_authenticated:
      abort(401)
    if current_user.role != "admin":
      abort(403)
    data = request.get_json()
    name = data.get("name")
    ingredient = Ingredients(name=name)
    db.session.add(ingredient)
    db.session.commit()
    return jsonify({"message": "Successfully added new ingredient!"}), 201


@routes.route("/login_check", methods=["GET"])
@login_required
def login_check() -> tuple[Response, int]:
  """ Endpoint used in development for checking if user is logged in. """
  return jsonify({"message": "User is logged in!"}), 200
