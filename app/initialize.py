from flask import Flask
from app import api, config
from app.infrastructure import databases
from dotenv import load_dotenv
import os

load_dotenv()

web_app = Flask(__name__)
api.create_api(web_app)
web_app.config['DATABASE_URL'] = os.environ['DATABASE_URL']
web_app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
web_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#web_app.config.from_object(config)
databases.register_orm(web_app)

