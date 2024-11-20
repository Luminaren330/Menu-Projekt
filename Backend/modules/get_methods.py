""" API GET functions. """
from datetime import datetime, timedelta

from flask import request
from sqlalchemy import or_, and_

from . import db
from .models import (
  Categories, Ingredients, Tables, Orders, Dishes, OrderItems, Reviews
)


def get_categories() -> dict:
  """ Returns dictionary of categories. """
  categories = Categories.query.with_entities(Categories.name).all()
  response = {"count": len(categories), "records": []}
  categories_to_return = [{"name": category.name} for category in categories]
  response["records"] = categories_to_return
  return response


def get_ingredients() -> dict:
  """ Returns dictionary of ingredients. """
  ingredients = Ingredients.query.with_entities(Ingredients.name).all()
  response = {"count": len(ingredients), "records": []}
  ingredients_to_return = [
    {"name": ingredient.name} for ingredient in ingredients]
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
    "name": dish.name,
    "category": dish.category.name,
    "ingredients": [ingredient.name for ingredient in dish.ingredients],
    "price": dish.price,
    "photo_url": dish.photo_url,
    "description": dish.description
  } for dish in dishes]
  response["records"] = dishes_to_return
  return response


def get_orders_to_return(orders: tuple) -> list:
  """ Generates list of orders to return. """
  return [{
      "table_id":
      order.table_id,
      "total_price":
      order.total_price,
      "order_status":
      order.order_status,
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
          "quantity":
          order_item.quantity,
          "price_per_dish":
          order_item.price,
      } for order_item in OrderItems.query.filter_by(
          order_id=order.order_id).all()],
      "order_date":
      order.order_date.strftime("%Y-%m-%d %H:%M:%S"),
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
    "dish": review.dish.name,
    "user": review.account.email,
    "stars": review.stars,
    "comment": review.comment
  } for review in reviews]
  response["records"] = reviews_to_return
  return response
