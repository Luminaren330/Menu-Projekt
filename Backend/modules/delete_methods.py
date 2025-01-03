""" API DELETE functions. """
import sqlalchemy.exc
from flask import request, session

from .models import (
  Categories, Ingredients, Tables, Dishes, dishes_ingredients, Orders, Reviews,
  OrderItems, Accounts, Employee, Clients, Cart
)
from . import db


def delete_user() -> [str, int]:
  """ Deletes user from the database. """
  user_id = request.args.get("id")
  if not user_id:
    return "Missing 'user_id' parameter", 404
  user = Accounts.query.get(user_id)
  if not user:
    return "User not found!", 400
  if user.role == "client":
    client = Clients.query.filter_by(account_id=user_id).first()
    db.session.delete(client)
  elif user.role == "employee":
    employee = Employee.query.filter_by(account_id=user_id).first()
    db.session.delete(employee)
  db.session.delete(user)
  db.session.commit()
  return f"User with id = {user.account_id} deleted successfully!", 200


def delete_category() -> [str, int]:
  """ Deletes category from the database. """
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
  item_id = request.args.get("id")
  if not item_id:
    return "Missing 'item_id' parameter", 404
  item = Cart.query.filter_by(cart_id=item_id).first()
  if not item:
    return f"There is no item with id = {item_id} in a cart!", 400
  db.session.delete(item)
  db.session.commit()
  return f"Item with id {item_id} deleted successfully!", 200


def delete_order() -> [str, int]:
  """ Deletes order from the database. """
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
  review_id = request.args.get("id")
  if not review_id:
    return "Missing 'review_id' parameter", 404
  review = Reviews.query.get(review_id)
  if not review:
    return "Review not found!", 400
  db.session.delete(review)
  db.session.commit()
  return f"Review with id {review.review_id} deleted successfully!", 200
