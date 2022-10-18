import imp
from flask_sqlalchemy import SQLAlchemy

db = None

def register_orm(web_app):
    global db 
    db = SQLAlchemy(web_app)

def register_migrations():   
    import app.models.areas
    import app.models.general_info
    db.create_all()
