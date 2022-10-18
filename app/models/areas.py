from app.infrastructure.databases import db
from geoalchemy2 import Geometry, functions
from sqlalchemy import func

class FarmAreaModel(db.Model):    
    __tablename__ = 'farm_areas'

    farm_id = db.Column(db.Integer, primary_key=True)
    nome_fazenda = db.Column(db.String(100))
    area = db.Column(db.Float(precision=2))
    state_id = db.Column(db.Integer, db.ForeignKey('states.state_id'))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.city_id'))
    geometry = db.Column(Geometry('MULTIPOLYGON', 3857))


    farm_protected_reserve = db.relationship('FarmReserveModel', backref='farm_protected')
    pol = db.column_property(func.ST_AsText(geometry))

    def __repr__(self):
        return '<FarmAreaModel %s>' % self.farm_id

    def as_json(self):
        #pol = db.column_property(func.ST_AsGeoJSON(self.geometry))
        return {'id': self.farm_id, 'nome_fazenda': self.nome_fazenda, 'area': self.area, 'geometry': self.pol}

    @classmethod
    def find_by_id(cls, farm_id):
        #wkt_geom = db.session.query(functions.ST_AsText(FarmAreaModel.geometry))
        print(FarmAreaModel.geometry)
        #print(wkt_geom)
        #return db.session.query(functions.ST_AsText(cls.geometry))        
        return cls.query.filter_by(farm_id=farm_id).first()


class FarmReserveModel(db.Model):
    __tablename__ = 'farm_reserves'

    fpr_id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farm_areas.farm_id'))
    area = db.Column(db.Float(precision=2))
    area_type = db.Column(db.String(20))
    geometry = db.Column(Geometry('MULTIPOLYGON', 3857))

    pol = db.column_property(func.ST_AsText(geometry))

    def as_json(self):
        return {'fpr_id': self.fpr_id, 'farm_id': self.farm_id, 'area': self.area, 'area_type': self.area_type, 'geometry': self.pol}

    @classmethod
    def find_by_id(cls, farm_id):        
        reserve_list = []
        areas = cls.query.filter_by(farm_id=farm_id).all()
        for area in areas:
            reserve_list.append(area.as_json())
        return reserve_list

