""" Models file. """
from datetime import datetime

from flask_login import UserMixin

from . import db


class Accounts(db.Model, UserMixin):
  """ Accounts table configuration. """
  account_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(50), nullable=False)
  role = db.Column(db.String(50), nullable=False)

  def __init__(self, email: str, password: str, role: str) -> None:
    """ Class constructor """
    self.email = email
    self.password = password
    self.role = role

  def __repr__(self) -> str:
    """ Returns user email. """
    return f"User('{self.email}')"

  def get_id(self) -> int:
    """ Returns account id. """
    return self.account_id


class Clients(db.Model, UserMixin):
  """ Clients table configuration. """
  client_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  account_id = db.Column(db.Integer, db.ForeignKey("accounts.account_id"),
                         nullable=False)
  firstname = db.Column(db.String(70), nullable=False)
  lastname = db.Column(db.String(150), nullable=False)
  telephone = db.Column(db.String(15), nullable=False)

  account = db.relationship("Accounts", backref="clients", lazy=True)

  def __init__(
    self, account_id: int, firstname: str, lastname: str, telephone: str
  ) -> None:
    """ Class constructor """
    self.account_id = account_id
    self.firstname = firstname
    self.lastname = lastname
    self.telephone = telephone

  def __repr__(self) -> str:
    """ Returns user first name and last name. """
    return f"Client('{self.firstname}', '{self.lastname}')"

  def get_id(self) -> int:
    """ Returns client id. """
    return self.client_id


class Employee(db.Model, UserMixin):
  """ Employee table configuration. """
  employee_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  account_id = db.Column(db.Integer, db.ForeignKey("accounts.account_id"),
                         nullable=False)
  firstname = db.Column(db.String(70), nullable=False)
  lastname = db.Column(db.String(150), nullable=False)
  telephone = db.Column(db.String(15), nullable=False)
  position = db.Column(db.String(40), nullable=False)
  is_available = db.Column(db.Boolean, default=True, nullable=False)

  account = db.relationship("Accounts", backref="employee", lazy=True)

  def __init__(
      self, account_id: int, firstname: str, lastname: str, telephone: str,
      position: str, is_available: bool
  ) -> None:
    """ Class constructor """
    self.account_id = account_id
    self.firstname = firstname
    self.lastname = lastname
    self.telephone = telephone
    self.position = position
    self.is_available = is_available

  def __repr__(self) -> str:
    """ Returns user first name and last name. """
    return f"Employee('{self.firstname}', '{self.lastname}')"

  def get_id(self) -> int:
    """ Returns employee id. """
    return self.employee_id


class Categories(db.Model, UserMixin):
  """ Categories table configuration. """
  category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(150), nullable=False)

  def __init__(self, name: str) -> None:
    """ Class constructor """
    self.name = name

  def __repr__(self) -> str:
    """ Returns category name. """
    return f"Category('{self.name}')"

  def get_id(self) -> int:
    """ Returns category id. """
    return self.category_id


dishes_ingredients = db.Table(
  'dishes_ingredients',
  db.Column('dish_id', db.Integer, db.ForeignKey('dishes.dish_id'),
            primary_key=True),
  db.Column('ingredient_id', db.Integer,
            db.ForeignKey('ingredients.ingredient_id'), primary_key=True)
)


class Dishes(db.Model, UserMixin):
  """ Dishes table configuration. """
  dish_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  ingredient_id = db.Column(db.Integer,
                            db.ForeignKey("ingredients.ingredient_id"),
                            nullable=False)
  category_id = db.Column(db.Integer, db.ForeignKey("categories.category_id"),
                          nullable=False)
  name = db.Column(db.String(70), nullable=False)
  price = db.Column(db.Float, nullable=False)
  photo_url = db.Column(db.String(15), nullable=False)
  description = db.Column(db.String(40), nullable=False)

  ingredients = db.relationship("Ingredients", secondary=dishes_ingredients,
                                backref="dishes", lazy="dynamic")
  category = db.relationship("Categories", backref="dishes", lazy=True)

  def __init__(
      self, dish_id: int, ingredient_id: int, category_id: int, name: str,
      price: float, photo_url: str, description: str
  ) -> None:
    """ Class constructor """
    self.dish_id = dish_id
    self.ingredient_id = ingredient_id
    self.category_id = category_id
    self.name = name
    self.price = price
    self.photo_url = photo_url
    self.description = description

  def __repr__(self) -> str:
    """ Returns dish name and price. """
    return f"Dish('{self.name}', '{self.price}')"

  def get_id(self) -> int:
    """ Returns dish id. """
    return self.dish_id


class Ingredients(db.Model, UserMixin):
  """ Ingredients table configuration. """
  ingredient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(70), nullable=False)

  def __init__(self, name: str) -> None:
    """ Class constructor """
    self.name = name

  def __repr__(self) -> str:
    """ Returns ingredient name. """
    return f"Ingredient('{self.name}')"

  def get_id(self) -> int:
    """ Returns ingredient id. """
    return self.ingredient_id


class OrderItems(db.Model, UserMixin):
  """ Order_items table configuration. """
  item_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  order_id = db.Column(db.Integer, db.ForeignKey("orders.order_id"),
                       nullable=False)
  dish_id = db.Column(db.Integer, db.ForeignKey("dishes.dish_id"),
                      nullable=False)
  quantity = db.Column(db.Integer, nullable=False)
  price = db.Column(db.Float, nullable=False)

  order = db.relationship("Orders", backref="order_items", lazy=True)
  dish = db.relationship("Dishes", backref="order_items", lazy=True)

  def __init__(
      self, item_id: int, order_id: int, dish_id: int, qunatity: int,
      price: float
  ) -> None:
    """ Class constructor """
    self.item_id = item_id
    self.order_id = order_id
    self.dish_id = dish_id
    self.quantity = qunatity
    self.price = price

  def __repr__(self) -> str:
    """ Returns order items quantity and price. """
    return f"OrderItems('{self.quantity}', '{self.price}')"

  def get_id(self) -> int:
    """ Returns order item id. """
    return self.item_id


class Orders(db.Model, UserMixin):
  """ Orders table configuration. """
  order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  table_id = db.Column(db.Integer, db.ForeignKey("tables.table_id"),
                       nullable=True)
  account_id = db.Column(db.Integer, db.ForeignKey("accounts.account_id"),
                         nullable=False)
  total_price = db.Column(db.Float, nullable=False)
  take_away_time = db.Column(db.DateTime, nullable=True)
  table_reservation_start_time = db.Column(db.DateTime, nullable=True)
  table_reservation_end_time = db.Column(db.DateTime, nullable=True)
  order_status = db.Column(db.String(50), nullable=False)
  order_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
  table = db.relationship("Tables", backref="orders", lazy=True)
  account = db.relationship("Accounts", backref="orders", lazy=True)

  def __init__(
      self, order_id: int, table_id: int, account_id: int, total_price: float,
      take_away: bool, order_status: str, order_date: datetime,
      update_date: datetime
  ) -> None:
    """ Class constructor """
    self.order_id: order_id
    self.table_id = table_id
    self.account_id = account_id
    self.total_price = total_price
    self.take_away = take_away
    self.order_status = order_status
    self.order_date = order_date
    self.update_date = update_date

  def __repr__(self) -> str:
    """ Returns order total price and order date. """
    return f"Order('{self.total_price}', '{self.order_date}')"

  def get_id(self) -> int:
    """ Returns order id. """
    return self.order_id


class Reviews(db.Model, UserMixin):
  """ Reviews table configuration. """
  review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  dish_id = db.Column(db.Integer, db.ForeignKey("dishes.dish_id"),
                      nullable=False)
  account_id = db.Column(db.Integer, db.ForeignKey("accounts.account_id"),
                         nullable=False)
  stars = db.Column(db.Float, nullable=False)
  comment = db.Column(db.String(150), nullable=False, default=False)

  dish = db.relationship("Dishes", backref="reviews", lazy=True)
  account = db.relationship("Accounts", backref="reviews", lazy=True)

  def __init__(
    self, review_id: int, dish_id: int, account_id: int, stars: float,
    comment: str
  ) -> None:
    """ Class constructor """
    self.review_id = review_id
    self.dish_id = dish_id
    self.account_id = account_id
    self.stars = stars
    self.comment = comment

  def __repr__(self) -> str:
    """ Returns reviews stars and comment. """
    return f"Review('{self.stars}', '{self.comment}')"

  def get_id(self) -> int:
    """ Returns review id. """
    return self.review_id


class Tables(db.Model, UserMixin):
  """ Tables table configuration. """
  table_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  capacity = db.Column(db.Integer, nullable=False)
  is_available = db.Column(db.Boolean, nullable=False, default=True)
  description = db.Column(db.String(150), nullable=True)

  def __init__(self, table_id: int, capacity: int, is_available: bool) -> None:
    """ Class constructor """
    self.table_id = table_id
    self.capacity = capacity
    self.is_available = is_available

  def __repr__(self) -> str:
    """ Returns table capacity and status. """
    return f"Table('{self.capacity}', '{self.is_available}')"

  def get_id(self) -> int:
    """ Returns table id. """
    return self.table_id
