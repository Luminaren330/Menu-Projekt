""" Routes file. """
from datetime import datetime, timedelta

from flask import request, jsonify, Blueprint, abort
from flask.wrappers import Response
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import or_, and_

from . import db
from .models import (
  Accounts, Clients, Employee, Categories, Ingredients, Tables, Dishes,
  Orders, OrderItems, Reviews
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
    start_time = request.args.get("start_time", datetime(1970, 1, 1, 0, 0, 0))
    if start_time != datetime(1970, 1, 1, 0, 0, 0):
      start_time = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    end_time = start_time + timedelta(hours=2)
    tables = (
      db.session.query(
        Tables.table_id, Tables.description, Tables.capacity,
        db.case(
          (
            or_(
              and_(
                Orders.table_reservation_start_time <= end_time,
                Orders.table_reservation_start_time >= start_time
              ),
              and_(
                Orders.table_reservation_end_time <= end_time,
                Orders.table_reservation_end_time >= start_time
              ),
              and_(
                Orders.table_reservation_start_time <= start_time,
                Orders.table_reservation_end_time >= end_time
              )
            ),
            False
          ),
          else_=True
        ).label("is_available")
      )
    ).outerjoin(Orders, Tables.table_id == Orders.table_id).all()
    response = {"count": len(tables), "records": []}
    tables_to_return = [
      {
        "table_id": table.table_id,
        "capacity": table.capacity,
        "description": table.description,
        "is_available": table.is_available
      } for table in tables]
    response["records"] = tables_to_return
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
    dishes = Dishes.query.all()
    response = {"count": len(dishes), "records": []}
    dishes_to_return = [{
      "name": dish.name,
      "category": dish.category.name,
      "ingredients": [ingredient.name for ingredient in dish.ingredients],
      "price": dish.price,
      "photo_url": dish.photo_url,
      "description": dish.description
    } for dish in dishes]
    response["records"] = dishes_to_return
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
    try:
      take_away = request.args.get("take_away", None).lower()
    except AttributeError:
      take_away = None
    try:
      account_id = request.args.get("account_id", None).lower()
    except AttributeError:
      account_id = None
    conditions = []

    if take_away == "true":
      conditions.append(Orders.take_away_time.isnot(None))
    elif take_away == "false":
      conditions.append(Orders.take_away_time.is_(None))
    if account_id:
      conditions.append(Orders.account_id == account_id)

    orders = Orders.query.with_entities(
      Orders.order_id, Orders.table_id, Orders.total_price,
      Orders.order_status, Orders.take_away_time,
      Orders.table_reservation_start_time, Orders.table_reservation_end_time,
      Orders.order_date
    ).filter(*conditions).all()
    response = {"count": len(orders), "records": []}
    orders_to_return = [
      {
        "table_id": order.table_id,
        "total_price": order.total_price,
        "order_status": order.order_status,
        "take_away_time": order.take_away_time.strftime("%Y-%m-%d %H:%M:%S")
        if order.take_away_time else None,
        "table_reservation_start_time": order.table_reservation_start_time.
        strftime("%Y-%m-%d %H:%M:%S") if order.table_reservation_start_time
        else None,
        "table_reservation_end_time": order.table_reservation_end_time.
        strftime("%Y-%m-%d %H:%M:%S") if order.table_reservation_end_time
        else None,
        "order_items": [
          {
            "dish_name": Dishes.query.filter_by(
              dish_id=order_item.dish_id).first().name,
            "quantity": order_item.quantity,
            "price_per_dish": order_item.price
          }
          for order_item in OrderItems.query.filter_by(
            order_id=order.order_id).all()],
        "order_date": order.order_date.strftime("%Y-%m-%d %H:%M:%S")
      } for order in orders]
    response["records"] = orders_to_return
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
    dish_id = request.args.get("dish_id")
    reviews = Reviews.query.filter_by(dish_id=dish_id).all()
    response = {"count": len(reviews), "records": []}
    reviews_to_return = [{
      "dish": review.dish.name,
      "user": review.account.email,
      "stars": review.stars,
      "comment": review.comment
    } for review in reviews]
    response["records"] = reviews_to_return
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
