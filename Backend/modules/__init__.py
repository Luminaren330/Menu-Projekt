""" Initialization file. """
import os
from datetime import timedelta
from typing import Any

from flask import Flask, jsonify
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv


load_dotenv()
db = SQLAlchemy()


def create_app() -> Flask:
  """ Creates and configures backend. """
  from .routes import routes
  from .models import Accounts

  app = Flask(__name__)
  db_user = os.getenv("DB_USER")
  db_password = os.getenv("DB_PASSWORD")
  db_url = os.getenv("DB_URL")
  db_dbname = os.getenv("DB_DBNAME")
  app.config[
    "SQLALCHEMY_DATABASE_URI"
  ] = f"postgresql+psycopg2://{db_user}:{db_password}@{db_url}/{db_dbname}"
  app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
  app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=30)
  db.init_app(app)

  app.register_blueprint(routes, url_prefix="/")
  with app.app_context():
    db.create_all()

  login_manager = LoginManager()
  login_manager.login_view = 'routes.login'
  login_manager.init_app(app)

  @login_manager.user_loader
  def load_user(user_id: int) -> Any:
    """ Returns user by given user id. """
    return Accounts.query.get(int(user_id))

  @login_manager.unauthorized_handler
  def unauthorized() -> tuple[Response, int]:
    """ Returns response message and status code when user is unauthorized. """
    return jsonify({"message": "User is not logged in!"}), 401

  return app
