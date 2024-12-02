""" API PATCH endpoints """


from flask import request, session
from flask_login import current_user

from .models import (
  Categories, Ingredients, Tables, Dishes, dishes_ingredients, Orders, Reviews,
  OrderItems
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
