""" API GET functions. """
from datetime import datetime, timedelta

from flask import request, session
from sqlalchemy import or_, and_

from . import db
from .models import (
  Categories, Ingredients, Tables, Orders, Dishes, OrderItems, Reviews,
  Accounts, Employee, Clients, Cart
)


def get_users() -> dict:
  """ Return dictionary of users. """
  all_accounts = Accounts.query.all()
  clients_accounts = db.session.query(Accounts, Clients).join(
    Clients, Accounts.account_id == Clients.account_id).all()
  employee_accounts = db.session.query(Accounts, Employee).join(
    Employee, Accounts.account_id == Employee.account_id)

  admins_to_return = [{
      "account_id": record.account_id,
      "email": record.email,
      "role": record.role
    }
    for record in all_accounts if record.role == "admin"
  ]
  response = {
    "admin_count": len(admins_to_return),
    "admin_records": admins_to_return}
  clients_to_return = [{
    "account_id": record.account_id,
    "email": record.email,
    "role": record.role,
    "firstname": client.firstname,
    "lastname": client.lastname,
    "telephone": client.telephone
  }
    for record, client in clients_accounts if record.role == "client"
  ]
  response["client_count"] = len(clients_to_return)
  response["client_records"] = clients_to_return
  employee_to_return = [{
    "account_id": record.account_id,
    "email": record.email,
    "role": record.role,
    "firstname": employee.firstname,
    "lastname": employee.lastname,
    "telephone": employee.telephone,
    "position": employee.position,
    "description": employee.description,
    "is_available": employee.is_available
  }
    for record, employee in employee_accounts if record.role == "employee"
  ]
  response["employee_count"] = len(employee_to_return)
  response["employee_records"] = employee_to_return
  return response


def get_categories() -> dict:
  """ Returns dictionary of categories. """
  categories = Categories.query.with_entities(
    Categories.category_id, Categories.name).all()
  response = {"count": len(categories), "records": []}
  categories_to_return = [
    {"category_id": category.category_id, "name": category.name}
    for category in categories]
  response["records"] = categories_to_return
  return response


def get_ingredients() -> dict:
  """ Returns dictionary of ingredients. """
  ingredients = Ingredients.query.with_entities(
    Ingredients.name, Ingredients.ingredient_id).all()
  response = {"count": len(ingredients), "records": []}
  ingredients_to_return = [
    {"ingredient_id": ingredient.ingredient_id, "name": ingredient.name}
    for ingredient in ingredients]
  response["records"] = ingredients_to_return
  return response


def get_tables() -> dict:
  """ Returns dictionary of tables. """
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
  return response


def get_dishes() -> dict:
  """ Returns dictionary of dishes. """
  dishes = Dishes.query.all()
  response = {"count": len(dishes), "records": []}
  dishes_to_return = [{
    "dish_id": dish.dish_id,
    "name": dish.name,
    "category": dish.category.name,
    "ingredients": [ingredient.name for ingredient in dish.ingredients],
    "price": dish.price,
    "photo_url": dish.photo_url,
    "description": dish.description
  } for dish in dishes]
  response["records"] = dishes_to_return
  return response


def get_cart() -> dict:
  """ Returns dictionary of order items. """
  user_id = request.args.get("user_id")
  cart = Cart.query.filter_by(account_id=user_id).all()
  if cart:
    order_items_to_return = {"count": len(cart), "records": []}
    for item in cart:
      item_id = item.cart_id
      dish = Dishes.query.get(item.dish_id)
      dish_name = dish.name
      dish_price = dish.price
      dish_photo = dish.photo_url
      dish_desc = dish.description
      quantity = item.quantity
      order_items_to_return["records"].append({
        "item_id": item_id,
        "dish_id": item.dish_id,
        "dish_name": dish_name,
        "price_per_item": dish_price,
        "photo_url": dish_photo,
        "description": dish_desc,
        "quantity": quantity
      })
    return order_items_to_return
  else:
    response = {"count": 0, "records": []}
    return response


def get_orders_to_return(orders: tuple) -> list:
  """ Generates list of orders to return. """
  return [{
    "order_id": order.order_id,
    "table_id": order.table_id,
    "total_price": order.total_price,
    "order_status": order.order_status,
    "take_away_time": (order.take_away_time.strftime("%Y-%m-%d %H:%M:%S")
                       if order.take_away_time else None),
    "table_reservation_start_time":
    (order.table_reservation_start_time.strftime("%Y-%m-%d %H:%M:%S")
     if order.table_reservation_start_time else None),
    "table_reservation_end_time":
    (order.table_reservation_end_time.strftime("%Y-%m-%d %H:%M:%S")
     if order.table_reservation_end_time else None),
    "order_items": [{
      "dish_name":
      Dishes.query.filter_by(dish_id=order_item.dish_id).first().name,
      "quantity": order_item.quantity,
      "price_per_dish": order_item.price,
    } for order_item in OrderItems.query.filter_by(
      order_id=order.order_id).all()],
    "order_date": order.order_date.strftime("%Y-%m-%d %H:%M:%S"),
  } for order in orders]


def get_orders() -> dict:
  """ Return dictionary of orders. """
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
  orders_to_return = get_orders_to_return(orders)
  response["records"] = orders_to_return
  return response


def get_reviews() -> dict:
  """ Returns dictionary of reviews. """
  dish_id = request.args.get("dish_id")
  reviews = Reviews.query.filter_by(dish_id=dish_id).all()
  response = {"count": len(reviews), "records": []}
  reviews_to_return = [{
    "review_id": review.review_id,
    "dish": review.dish.name,
    "user": review.account.email,
    "stars": review.stars,
    "comment": review.comment
  } for review in reviews]
  response["records"] = reviews_to_return
  return response
