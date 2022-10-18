from app.infrastructure.databases import db

class StatesModel(db.Model):
    __tablename__ = 'states'

    state_id = db.Column(db.Integer, primary_key=True)    
    uf = db.Column(db.String(2))
    state = db.Column(db.String(50))

    farms = db.relationship('FarmAreaModel', backref='farm_area')
    cities = db.relationship('CitiesModel', backref='cities')

    def as_json(self):        
        return {'state_id': self.state_id, 'uf': self.uf, 'state': self.state}

    @classmethod
    def list_all(cls):
        states_list = []
        states = cls.query.all()
        for state in states:
            states_list.append(state.as_json())
        return states_list

class CitiesModel(db.Model):
    __tablename__ = 'cities'

    city_id = db.Column(db.Integer, primary_key=True)
    state_id = db.Column(db.Integer, db.ForeignKey('states.state_id'))
    uf = db.Column(db.String(2))
    city = db.Column(db.String(100))
    

    farms = db.relationship('FarmAreaModel', backref='farm_areas')

    def as_json(self):        
        return {'city_id': self.city_id, 'state_id': self.state_id, 'uf': self.uf, 'city': self.city}

    @classmethod
    def list_cities_by_state(cls, state_id):
        cities_list = []
        cities = cls.query.filter_by(state_id=state_id).all()
        for city in cities:
            cities_list.append(city.as_json())
        return cities_list
