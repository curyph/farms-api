from flask_restful import Resource
from app.collections.download_sentinel_hub import SentinelImages
from flask import request
from app.domain.process_inputs import HandleUserInput
from app.models import areas, general_info

class InitResource(Resource):
    def get(self):
        return {'message': 'Testing API'}

class HomeResource(Resource):
    def get(self):        
        return 'home'

class SentinelResource(Resource):
    def get(self):
        sentinel = SentinelImages.createSentinelInstance()
        sentinel.start_process()
        return {'Image Status': 'Downloaded'}

class FarmUploadResource(Resource):    
    
    def post(self):
        try:
            file = request.files['files[]']
            state_id = request.args['state_id']
            city_id = request.args['city_id']            
            user_input = HandleUserInput(file, state_id, city_id)
            user_input.process_file()
            return {'message': 'File uploaded Successfully'}
        except Exception as ex:            
            return {'message': str(ex)}
         

class ListFarmGeometryResource(Resource):
    # Adicionar customer_id futuramente
    def get(self, state_id, city_id):
        print(request.args)
        # print(request.headers)
        # dct = {arg: value for (arg, value) in request.args.items() if value != 'undefined'}

        # print(dct)
        # print(request.json)


        area = areas.FarmAreaModel.find_by_id(state_id, city_id)
        if area:            
            return area
        return {'Message': 'area not found'}

    def post(self): 
        print(request.json)


class ListFarmReservesResource(Resource):
    def get(self, farm_id):
        area = areas.FarmReserveModel.find_by_id(farm_id)    
        if area:            
            return area
        return {'Message': 'area not found'}

class ListStates(Resource):
    def get(self):
        states = general_info.StatesModel.list_all()       
        if states:
            return states
        return {'message': 'No states found'}


class ListCities(Resource):
    def get(self, state_id):
        cities = general_info.CitiesModel.list_cities_by_state(state_id)
        return cities