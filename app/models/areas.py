from app.infrastructure.databases import db
from geoalchemy2 import Geometry

class FarmAreaModel(db.Model):
    print(db)
    __tablename__ = 'farm_areas'

    id = db.Column(db.Integer, primary_key=True)
    nome_fazenda = db.Column(db.String(100))
    area = db.Column(db.Float(precision=2))
    geometry = db.Column(Geometry('MULTIPOLYGON', 3857))



