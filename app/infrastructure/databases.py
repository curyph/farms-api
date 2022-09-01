import imp
from flask_sqlalchemy import SQLAlchemy

db = None

def register_orm(web_app):
    global db 
    db = SQLAlchemy(web_app)

def register_migrations():
    from app.models.areas import FarmAreaModel
    db.create_all()
