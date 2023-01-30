import imp
from flask_sqlalchemy import SQLAlchemy

db = None

def register_orm(web_app):
    global db 
    db = SQLAlchemy(web_app)

def register_migrations(web_app):   
    import app.models.areas
    import app.models.general_info
    with web_app.app_context():
        db.create_all()