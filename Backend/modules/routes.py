""" Routes file. """
from flask import request, jsonify, Blueprint
from flask.wrappers import Response
from flask_login import login_required

from .get_methods import (
  get_categories, get_ingredients, get_tables, get_dishes, get_orders,
  get_reviews, get_cart
)
from .post_methods import (
  register_user, log_in_user, log_out_user, add_new_category,
  add_new_ingredient, add_new_table, add_new_dish, add_new_review,
  add_new_order_item, add_new_order
)


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
  register_user()
  return jsonify({"message": "User registered successfully!"}), 201


@routes.route("/login", methods=["POST"])
def login() -> tuple[Response, int]:
  """
  User login endpoint.
  To login user pass to the endpoint body following data: email, password.
  """
  message, status_code = log_in_user()
  return jsonify({"message": message}), status_code


@routes.route("/logout", methods=["POST"])
@login_required
def logout() -> tuple[Response, int]:
  """ User logout endpoint. """
  message, status_code = log_out_user()
  return jsonify({"message": message}), status_code


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
    response = get_categories()
    return jsonify(response), 200
  elif request.method == "POST":
    message, status_code = add_new_category()
    return jsonify({"message": message}), status_code


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
    response = get_ingredients()
    return jsonify(response), 200
  elif request.method == "POST":
    message, status_code = add_new_ingredient()
    return jsonify({"message": message}), status_code


@routes.route("/tables", methods=["GET", "POST"])
def manage_tables() -> tuple[Response, int]:
  """
  Endpoint used to manage tables.
  To add new table use POST method. Pass the following data to the endpoint
  body: capacity and description.
  ONLY admin user can add new tables.
  To retrieve all tables use GET method. Authorized users
  can retrieve this data. You have to pass query param start_time
  (%Y-%m-%d %H:%M:%S).
  """
  if request.method == "GET":
    response = get_tables()
    return jsonify(response), 200
  elif request.method == "POST":
    message, status_code = add_new_table()
    return jsonify({"message": message}), status_code


@routes.route("/dishes", methods=["GET", "POST"])
def manage_dishes() -> tuple[Response, int]:
  """
  Endpoint used to manage dishes.
  To add new dish use POST method. Pass the following data to the endpoint
  category (name), ingredients (list of names), name, price, photo_url and
  description.
  Admin and employee user can add new dishes.
  To retrieve all dishes use GET method. Unauthorized users
  can retrieve this data.
  """
  if request.method == "GET":
    response = get_dishes()
    return jsonify(response), 200
  elif request.method == "POST":
    message, status_code = add_new_dish()
    return jsonify({"message": message}), status_code


@routes.route("/carts", methods=["GET", "POST"])
def manage_carts() -> tuple[Response, int]:
  """
  Endpoint used to manage order cart.
  To add order item to the cart user POST method. Pass the following data to
  the endpoint: dish_id, quantity.
  To retrieve all items in the cart use GET method.
  Only authorized users can add new items to the cart and retrieve this data.
  """
  if request.method == "GET":
    response = get_cart()
    return jsonify(response), 200
  elif request.method == "POST":
    message, status_code = add_new_order_item()
    return jsonify({"message": message}), status_code


@routes.route("/orders", methods=["GET", "POST"])
def manage_orders() -> tuple[Response, int]:
  """
  Endpoint used to manage orders.
  To add new order use POST method. Pass the following data to the endpoint:
  order to the table - table_id, table_reservation_start_time
  (%Y-%m-%d %H:%M:%S), dishes ([[dish_id, quantity, price per dish]],
  take away order - take_away_time (%Y-%m-%d %H:%M:%S), dishes.
  To retrieve all orders use GET method. You can retrieve only take_away orders
  or orders to the table passing query param ?take_away=true/false.
  To retrieve specific user's orders pass query param ?account_id=account_id.
  By not passing param all orders will be retrieved. Only authorized users can
  retrieve this data.
  """
  if request.method == "GET":
    response = get_orders()
    return jsonify(response), 200
  elif request.method == "POST":
    message, status_code = add_new_order()
    return jsonify({"message": message}), status_code


@routes.route("/reviews", methods=["GET", "POST"])
def manage_reviews() -> tuple[Response, int]:
  """
  Endpoint used to manage reviews.
  To add new review use POST method. Pass the following data to the endpoint
  dish_id, stars, comment. Only authorized users can add new review.
  To retrieve all reviews use GET method. You have to pass query param dish_id.
  """
  if request.method == "GET":
    response = get_reviews()
    return jsonify(response), 200
  elif request.method == "POST":
    message, status_code = add_new_review()
    return jsonify({"message": message}), status_code
