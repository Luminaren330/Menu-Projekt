""" Routes file. """
from datetime import datetime, timedelta

from flask import request, jsonify, Blueprint, abort
from flask.wrappers import Response
from flask_login import login_required, current_user

from . import db
from .models import (
  Categories, Ingredients, Tables, Dishes, Orders, OrderItems, Reviews
)
from .get_methods import (
  get_categories, get_ingredients, get_tables, get_dishes, get_orders,
  get_reviews
)
from .post_methods import (
  register_user, log_in_user, log_out_user, add_new_category
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
    if not current_user.is_authenticated:
      abort(401)
    if current_user.role != "admin":
      abort(403)
    data = request.get_json()
    capacity = data.get("capacity")
    description = data.get("description")
    table = Tables(
      capacity=capacity, description=description)
    db.session.add(table)
    db.session.commit()
    return jsonify({"message": "Successfully added new table!"}), 201


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
    if not current_user.is_authenticated:
      abort(401)
    if current_user.role not in ["admin", "employee"]:
      abort(403)
    data = request.get_json()
    category = data.get("category")
    ingredients = data.get("ingredients")
    name = data.get("name")
    price = data.get("price")
    photo_url = data.get("photo_url")
    description = data.get("description")

    category = Categories.query.filter_by(name=category).first()
    ingredients = Ingredients.query.filter(
      Ingredients.name.in_(ingredients)).all()
    dish = Dishes(
      category_id=category.category_id, name=name, price=price,
      photo_url=photo_url, description=description)
    dish.ingredients.extend(ingredients)

    db.session.add(dish)
    db.session.commit()
    return jsonify({"message": "Successfully added new dish!"}), 201


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
    if not current_user.is_authenticated:
      abort(401)
    data = request.get_json()
    # orders
    table_id = data.get("table_id")
    account_id = current_user.get_id()
    take_away_time = data.get("take_away_time")
    table_start_time = data.get("table_reservation_start_time")
    if take_away_time:
      take_away_time = datetime.strptime(
        take_away_time, "%Y-%m-%d %H:%M:%S")
      table_start_time = None
      table_end_time = None
    else:
      take_away_time = None
      table_start_time = datetime.strptime(
        table_start_time, "%Y-%m-%d %H:%M:%S")
      table_end_time = table_start_time + timedelta(hours=2)
    order_status = "new"

    # order items
    dishes = data.get("dishes")  # [[dish_id, quantity, price], ...]
    total_price = round(sum(dish[2] * dish[1] for dish in dishes), 2)
    order = Orders(
      table_id=table_id, account_id=account_id, total_price=total_price,
      take_away_time=take_away_time,
      table_start_time=table_start_time,
      table_end_time=table_end_time, order_status=order_status
    )
    db.session.add(order)
    db.session.flush()

    for dish in dishes:
      dish_id = dish[0]
      quantity = dish[1]
      price = dish[2]
      order_item = OrderItems(
        order_id=order.order_id, dish_id=dish_id, quantity=quantity,
        price=price
      )
      db.session.add(order_item)

    db.session.commit()

    return jsonify({"message": "Successfully added new order!"}), 201


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
    if not current_user.is_authenticated:
      abort(401)
    data = request.get_json()
    dish_id = data.get("dish_id")
    account_id = current_user.get_id()
    stars = data.get("stars")
    comment = data.get("comment")

    review = Reviews(
      dish_id=dish_id, account_id=account_id, stars=stars, comment=comment)
    db.session.add(review)
    db.session.commit()
    return jsonify({"message": "Successfully added new review!"}), 201
