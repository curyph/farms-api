from app.infrastructure.databases import db
from geoalchemy2 import Geometry, functions
from sqlalchemy import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class FarmAreaModel(db.Model):    
    __tablename__ = 'farm_areas'

    farm_id = db.Column(db.Integer, primary_key=True)
    nome_fazenda = db.Column(db.String(100))
    area = db.Column(db.Float(precision=2))
    state_id = db.Column(db.Integer, db.ForeignKey('states.state_id'))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.city_id'))
    geometry = db.Column(Geometry('MULTIPOLYGON', 3857))

    farm_protected_reserve = db.relationship('FarmReserveModel', backref='farm_areas')
    #reserves = db.relationship('ReservesModel', primaryjoin='func.ST_intersects(foreign(FarmAreaModel.geometry), ReservesModel.geometry).as_comparison(1, 2)', backref='reserves', viewonly=True, uselist=True)
    farm_pedology = db.relationship('FarmPedologyModel', backref='farm_areas')

    pol = db.column_property(func.ST_AsText(geometry))

    def __repr__(self):
        return '<FarmAreaModel %s>' % self.farm_id

    def as_json(self):
        #pol = db.column_property(func.ST_AsGeoJSON(self.geometry))
        return {'id': self.farm_id, 'nome_fazenda': self.nome_fazenda, 'area': self.area, 'geometry': self.pol, 'reserves': [reserve.pol for reserve in self.reserves]}

    @classmethod
    def find_by_id(cls, state_id, city_id):
        #wkt_geom = db.session.query(functions.ST_AsText(FarmAreaModel.geometry))               
        #return db.session.query(functions.ST_AsText(cls.geometry)) 
        areas_list = []
        areas = cls.query.filter_by(state_id=state_id, city_id=city_id).all()
        for area in areas:
            areas_list.append(area.as_json())
        return areas_list


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


class ReservesModel(db.Model):
    __tablename__ = 'reserves'

    res_id = db.Column(db.Integer, primary_key=True)
    reserve_type = db.Column(db.String(100))
    geometry = db.Column(Geometry('MULTIPOLYGON', 3857))

    pol = db.column_property(func.ST_AsText(geometry))


class PedologyModel(db.Model):
    __tablename__ = 'pedology'

    ped_id = db.Column(db.Integer, primary_key=True)
    cod_symbol = db.Column(db.String(10))
    legend = db.Column(db.String(100))
    order = db.Column(db.String(25))
    suborder = db.Column(db.String(25))
    color_pattern = db.Column(db.String(10))
    geometry = db.Column(Geometry('POLYGON', 3857))

    geom = db.column_property(func.ST_AsText(geometry))

    farm_pedology = db.relationship('FarmPedologyModel', backref='pedology')

    #farm_pedology_new = db.relationship('FarmAreaModel', secondary=PedologyTeste, backref='PedologyModel')


class FarmPedologyModel(db.Model):
    __tablename__ = 'farm_pedology'

    farm_ped_id = db.Column(db.Integer, primary_key=True)
    ped_id = db.Column(db.Integer, db.ForeignKey('pedology.ped_id'))
    farm_id = db.Column(db.Integer, db.ForeignKey('farm_areas.farm_id'))
    cod_symbol = db.Column(db.String(10))
    legend = db.Column(db.String(100))
    order = db.Column(db.String(25))
    suborder = db.Column(db.String(25))
    color_pattern = db.Column(db.String(10))
    geometry = db.Column(Geometry('MULTIPOLYGON', 3857))

    geom = db.column_property(func.ST_AsText(geometry))