from flask import Flask
from app import api, config
from dotenv import load_dotenv

load_dotenv()

web_app = Flask(__name__)
api.create_api(web_app)
#web_app.config.from_object(config)


