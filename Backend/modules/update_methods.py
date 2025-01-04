""" API PATCH endpoints """
from datetime import datetime, timedelta

from flask import request, session

from .models import (
  Categories, Ingredients, Tables, Dishes, Orders, Reviews, Accounts,
  Employee, Clients, Cart
)
from . import db


def update_user() -> [str, int]:
  """ Updates user in the database. """
  user_id = request.args.get("id")
  user = Accounts.query.get(user_id)
  if user.role == "client":
    return update_client(user_id)
  if user.role == "employee":
    return update_employee(user_id)


def update_client(user_id: str) -> [str, int]:
  """ Updates client in the database. """
  data = request.get_json()
  user = Clients.query.filter_by(account_id=user_id).first()
  if not user:
    return "User not found!", 404
  if "firstname" in data:
    user.firstname = data.get("firstname")
  if "lastname" in data:
    user.lastname = data.get("lastname")
  if "telephone" in data:
    user.telephone = data.get("telephone")
  db.session.commit()
  return f"User with id {user.account_id} updated!", 200


def update_employee(user_id: str) -> [str, int]:
  """ Updates employee in the database. """
  data = request.get_json()
  user = Employee.query.filter_by(account_id=user_id).first()
  if not user:
    return "User not found!", 404
  if "firstname" in data:
    user.firstname = data.get("firstname")
  if "lastname" in data:
    user.lastname = data.get("lastname")
  if "telephone" in data:
    user.telephone = data.get("telephone")
  if "position" in data:
    user.position = data.get("position")
  if "is_available" in data:
    user.is_available = data.get("is_available")
  if "description" in data:
    user.description = data.get("description")
  db.session.commit()
  return f"User with id {user.account_id} updated!", 200


def update_category() -> [str, int]:
  """ Updates category in the database. """
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
  item_id = request.args.get("id")
  data = request.get_json()
  order_item = Cart.query.filter_by(cart_id=item_id).first()
  if not order_item:
    return f"There is no item with id = {item_id} in a cart!", 404
  if "dish_id" in data:
    dish_id = data.get("dish_id")
    try:
      dish = Dishes.query.get(dish_id)
      price = dish.price
    except AttributeError:
      return "Given dish id not found!", 404
    order_item.dish_id = dish_id
    order_item.price = price
  if "quantity" in data:
    quantity = data.get("quantity")
    order_item.quantity = quantity
  db.session.commit()
  return f"Order item with id {item_id} updated!", 200


def update_review() -> [str, int]:
  """ Updates table in the database. """
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
