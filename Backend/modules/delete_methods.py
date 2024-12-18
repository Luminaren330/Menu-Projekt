""" API DELETE functions. """
import sqlalchemy.exc
from flask import request, session
from flask_login import current_user

from .models import (
  Categories, Ingredients, Tables, Dishes, dishes_ingredients, Orders, Reviews,
  OrderItems
)
from . import db


def delete_category() -> [str, int]:
  """ Deletes category from the database. """
  if not current_user.is_authenticated:
    return "Only authorized users can delete a category!", 401
  if current_user.role != "admin":
    return "Only users with role 'admin' can delete a category!", 403
  category_id = request.args.get("id")
  if not category_id:
    return "Missing 'category_id' parameter", 404
  category = Categories.query.get(category_id)
  if not category:
    return "Category not found!", 400
  db.session.delete(category)
  try:
    db.session.commit()
  except sqlalchemy.exc.IntegrityError:
    return "There are dishes depending on this category!", 400
  return f"Category '{category.name}' deleted successfully!", 200


def delete_ingredient() -> [str, int]:
  """ Deletes ingredient from the database. """
  if not current_user.is_authenticated:
    return "Only authorized users can delete an ingredient!", 401
  if current_user.role != "admin":
    return "Only users with role 'admin' can delete an ingredient!", 403
  ingredient_id = request.args.get("id")
  if not ingredient_id:
    return "Missing 'ingredient_id' parameter", 404
  ingredient = Ingredients.query.get(ingredient_id)
  if not ingredient:
    return "Category not found!", 400
  db.session.delete(ingredient)
  db.session.commit()
  return f"Ingredient '{ingredient.name}' deleted successfully!", 200


def delete_table() -> [str, int]:
  """ Deletes table from the database. """
  if not current_user.is_authenticated:
    return "Only authorized users can delete a table!", 401
  if current_user.role != "admin":
    return "Only users with role 'admin' can delete a table!", 403
  table_id = request.args.get("id")
  if not table_id:
    return "Missing 'table_id' parameter", 404
  table = Tables.query.get(table_id)
  if not table:
    return "Table not found!", 400
  db.session.delete(table)
  db.session.commit()
  return f"Table with id {table.table_id} deleted successfully!", 200


def delete_dish() -> [str, int]:
  """ Deletes dish from the database. """
  if not current_user.is_authenticated:
    return "Only authorized users can delete a dish!", 401
  if current_user.role not in ["admin", "employee"]:
    return "Only users with role 'admin' or 'employee' can delete a dish!", 403
  dish_id = request.args.get("id")
  if not dish_id:
    return "Missing 'dish_id' parameter", 404
  dish = Dishes.query.get(dish_id)
  if not dish:
    return "Dish not found!", 400
  order_items = OrderItems.query.filter_by(dish_id=dish_id).all()
  for item in order_items:
    db.session.delete(item)
  reviews = Reviews.query.filter_by(dish_id=dish_id).all()
  for review in reviews:
    db.session.delete(review)
  dishes_ingredients.delete().where(dishes_ingredients.c.dish_id == dish_id)
  db.session.delete(dish)
  db.session.commit()
  return f"Dish '{dish.name}' deleted successfully!", 200


def delete_order_item() -> [str, int]:
  """ Deletes order item from the session. """
  if not current_user.is_authenticated:
    return "Only authorized users can delete an order item!", 401
  item_id = request.args.get("id")
  if not item_id:
    return "Missing 'item_id' parameter", 404
  items = session.get("cart", [])
  if not items:
    return "There is no items in a cart!", 400
  item_exists = any(item["item_id"] == int(item_id) for item in items)
  if not item_exists:
    return f"There is no item with id = {item_id} in a cart!", 400
  items = [item for item in items if item["item_id"] != int(item_id)]
  session["cart"] = items
  return f"Item with id {item_id} deleted successfully!", 200


def delete_order() -> [str, int]:
  """ Deletes order from the database. """
  if not current_user.is_authenticated:
    return "Only authorized users can delete an order!", 401
  order_id = request.args.get("id")
  if not order_id:
    return "Missing 'order_id' parameter", 404
  order = Orders.query.get(order_id)
  if not order:
    return "Order not found!", 400
  order_items = OrderItems.query.filter_by(order_id=order_id).all()
  for item in order_items:
    db.session.delete(item)
  db.session.delete(order)
  db.session.commit()
  return f"Order with id {order.order_id} deleted successfully!", 200


def delete_review() -> [str, int]:
  """ Deletes review from the database. """
  if not current_user.is_authenticated:
    return "Only authorized users can delete a review!", 401
  review_id = request.args.get("id")
  if not review_id:
    return "Missing 'review_id' parameter", 404
  review = Reviews.query.get(review_id)
  if not review:
    return "Review not found!", 400
  db.session.delete(review)
  db.session.commit()
  return f"Review with id {review.review_id} deleted successfully!", 200
