""" API PATCH endpoints """
from datetime import datetime, timedelta

from flask import request, session
from flask_login import current_user

from .models import (
  Categories, Ingredients, Tables, Dishes, Orders, Reviews, OrderItems
)
from . import db


def update_category() -> [str, int]:
  """ Updates category in the database. """
  if not current_user.is_authenticated:
    return "Only authorized users can update a category!", 401
  if current_user.role != "admin":
    return "Only users with role 'admin' can update a category!", 403
  category_id = request.args.get("id")
  data = request.get_json()
  category = Categories.query.get(category_id)
  if not category:
    return "Category not found!", 404
  if "name" in data:
    category.name = data.get("name")
  db.session.commit()
  return f"Category with id {category.category_id} updated!", 200


def update_ingredient() -> [str, int]:
  """ Updates ingredient in the database. """
  if not current_user.is_authenticated:
    return "Only authorized users can update an ingredient!", 401
  if current_user.role != "admin":
    return "Only users with role 'admin' can update an ingredient!", 403
  ingredient_id = request.args.get("id")
  data = request.get_json()
  ingredient = Ingredients.query.get(ingredient_id)
  if not ingredient:
    return "Ingredient not found!", 404
  if "name" in data:
    ingredient.name = data.get("name")
  db.session.commit()
  return f"Ingredient with id {ingredient.ingredient_id} updated!", 200


def update_table() -> [str, int]:
  """ Updates table in the database. """
  if not current_user.is_authenticated:
    return "Only authorized users can update a table!", 401
  if current_user.role != "admin":
    return "Only users with role 'admin' can update a table!", 403
  table_id = request.args.get("id")
  data = request.get_json()
  table = Tables.query.get(table_id)
  if not table:
    return "Table not found!", 404
  if "capacity" in data:
    table.capacity = data.get("capacity")
  if "description" in data:
    table.description = data.get("description")
  db.session.commit()
  return f"Table with id {table.table_id} updated!", 200


def update_dish() -> [str, int]:
  """ Updates dish in the database. """
  if not current_user.is_authenticated:
    return "Only authorized users can update a table!", 401
  if current_user.role not in ["admin", "employee"]:
    return "Only users with role 'admin' or 'employee' can update a dish!", 403
  dish_id = request.args.get("id")
  data = request.get_json()
  dish = Dishes.query.get(dish_id)
  if not dish:
    return "Dish not found!", 404
  if "category" in data:
    category = Categories.query.filter_by(name=data.get("category"))
    dish.category_id = category.category_id
  if "description" in data:
    dish.description = data.get("description")
  if "ingredients" in data:
    ingredients = Ingredients.query.filter(
      Ingredients.name.in_(data.get("ingredients"))).all()
    dish.ingredients = ingredients
  if "name" in data:
    dish.name = data.get("name")
  if "photo_url" in data:
    dish.photo_url = data.get("photo_url")
  if "price" in data:
    dish.price = data.get("price")
  db.session.commit()
  return f"Dish with id {dish.dish_id} updated!", 200


def update_order() -> [str, int]:
  """ Updates order in the database. """
  if not current_user.is_authenticated:
    return "Only authorized users can update an order!", 401
  order_id = request.args.get("id")
  data = request.get_json()
  order = Orders.query.get(order_id)
  if not order:
    return "Order not found!", 404
  if "table_id" in data:
    order.table_id = data.get("table_id")
  if "take_away_time" in data:
    order.take_away_time = data.get("take_away_time")
  if "table_reservation_start_time" in data:
    start = data.get("table_reservation_start_time")
    start = datetime.strptime(
      start, "%Y-%m-%d %H:%M:%S")
    end = start + timedelta(hours=2)
    order.table_reservation_start_time = start
    order.table_reservation_end_time = end
  if "order_status" in data:
    order.order_status = data.get("order_status")
  db.session.commit()
  return f"Order with id {order.order_id} updated!", 200


def update_order_item() -> [str, int]:
  """ Updates order item in the session. """
  if not current_user.is_authenticated:
    return "Only authorized users can update an order item!", 401
  item_id = request.args.get("id")
  data = request.get_json()
  items = session.get("cart", [])
  item_exists = any(item["item_id"] == int(item_id) for item in items)
  if not item_exists:
    return f"There is no item with id = {item_id} in a cart!", 404
  for item in items:
    if item["item_id"] == int(item_id):
      if "dish_id" in data:
        dish_id = data.get("dish_id")
        try:
          dish = Dishes.query.get(dish_id)
          price = dish.price
        except AttributeError:
          return "Given dish id not found!", 404
        item["dish_id"] = dish_id
        item["price"] = price
      if "quantity" in data:
        quantity = data.get("quantity")
        item["quantity"] = quantity
  session["cart"] = items
  return f"Order item with id {item_id} updated!", 200


def update_review() -> [str, int]:
  """ Updates table in the database. """
  if not current_user.is_authenticated:
    return "Only authorized users can update a review!", 401
  review_id = request.args.get("id")
  data = request.get_json()
  review = Reviews.query.get(review_id)
  if not review:
    return "Review not found!", 404
  if "stars" in data:
    review.stars = data.get("stars")
  if "comment" in data:
    review.comment = data.get("comment")
  db.session.commit()
  return f"Review with id {review.review_id} updated!", 200
