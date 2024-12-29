""" API POST functions. """
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import os

import sqlalchemy.exc
from flask import request, jsonify, session
from flask.wrappers import Response
from flask_login import login_user, logout_user

from . import db
from .models import (
  Accounts, Clients, Employee, Categories, Ingredients, Tables, Dishes,
  Orders, OrderItems, Reviews
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
  description = data.get("description")
  employee = Employee(account_id=user.account_id, firstname=firstname,
                      lastname=lastname, telephone=telephone,
                      position=position, is_available=is_available,
                      description=description)
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
    user_to_return = {
      "user_id": user.account_id,
      "email": user.email,
      "role": user.role
    }
    response = {
      "message": "Logged in successfully!",
      "user_data": user_to_return
    }
    return response, 200
  else:
    return "Login failed! Check email and password.", 401


def log_out_user() -> [str, int]:
  """ Logs out user. """
  logout_user()
  return "User logged out successfully!", 200


def add_new_category() -> [str, int]:
  """ Inserts new category to the database. """
  data = request.get_json()
  name = data.get("name")
  category = Categories(name=name)
  db.session.add(category)
  db.session.commit()
  return "Successfully added new category", 201


def add_new_ingredient() -> [str, int]:
  """ Inserts new ingredient to the database."""
  data = request.get_json()
  name = data.get("name")
  ingredient = Ingredients(name=name)
  db.session.add(ingredient)
  db.session.commit()
  return "Successfully added new ingredient!", 201


def add_new_table() -> [str, int]:
  """ Inserts new table to the database. """
  data = request.get_json()
  capacity = data.get("capacity")
  description = data.get("description")
  table = Tables(
    capacity=capacity, description=description)
  db.session.add(table)
  db.session.commit()
  return "Successfully added new table!", 201


def add_new_dish() -> [str, int]:
  """ Inserts new dish to the database. """
  category = request.form.get("category")
  ingredients = request.form.get("ingredients").split(",")
  name = request.form.get("name")
  price = float(request.form.get("price"))
  description = request.form.get("description")
  if photo := request.files.get("photo"):
    filename = secure_filename(photo.filename)
    save_path = os.path.join(os.getenv("UPLOAD_FOLDER"), filename)
    photo.save(save_path)
    photo_url = save_path
  else:
    photo_url = None
  category = Categories.query.filter_by(name=category).first()
  ingredients = Ingredients.query.filter(
    Ingredients.name.in_(ingredients)).all()
  dish = Dishes(
    category_id=category.category_id, name=name, price=price,
    photo_url=photo_url, description=description)
  dish.ingredients.extend(ingredients)

  db.session.add(dish)
  db.session.commit()
  return "Successfully added new dish!", 201


def add_new_order_item() -> [str, int]:
  """ Inserts new order item to the database. """
  data = request.get_json()
  dish_id = data.get("dish_id")
  quantity = data.get("quantity")
  try:
    dish = Dishes.query.get(dish_id)
    price = dish.price
  except AttributeError:
    return "Given dish id not found!", 400
  cart = session.get("cart", [])
  cart.append({
    "item_id": len(cart), "dish_id": dish_id, "quantity": quantity,
    "price": price
  })
  session["cart"] = cart
  return "Successfully added new cart!", 201


def add_new_order() -> [str, int]:
  """ Inserts new order to the database. """
  data = request.get_json()
  table_id = data.get("table_id")
  account_id = data.get("user_id")
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
  cart = session.get("cart", [])
  if not cart:
    return "Cart is empty", 400
  total_price = sum(item["price"] * item["quantity"] for item in cart)
  order = Orders(
    table_id=table_id, account_id=account_id, total_price=total_price,
    take_away_time=take_away_time,
    table_start_time=table_start_time,
    table_end_time=table_end_time, order_status=order_status
  )
  db.session.add(order)
  db.session.commit()

  for item in cart:
    order_item = OrderItems(
      order_id=order.order_id,
      dish_id=item['dish_id'],
      quantity=item['quantity'],
      price=item['price']
    )
    db.session.add(order_item)
  db.session.commit()
  session.pop("cart", None)
  return "Successfully added new order!", 201


def add_new_review() -> [str, int]:
  """ Inserts new review to the database. """
  data = request.get_json()
  dish_id = int(data.get("dish_id"))
  account_id = data.get("user_id")
  stars = data.get("stars")
  comment = data.get("comment")
  print(data)
  review = Reviews(
    dish_id=dish_id, account_id=account_id, stars=stars, comment=comment)
  db.session.add(review)
  try:
    db.session.commit()
  except sqlalchemy.exc.IntegrityError:
    return "Given dish id does not exist!", 400
  return "Successfully added new review!", 201
