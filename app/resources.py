from flask_restful import Resource
from app.collections.download_sentinel_hub import SentinelImages
from flask import request
from app.domain.process_inputs import HandleUserInput
from app.models import areas

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
            user_input = HandleUserInput(file)
            user_input.process_file()
            return {'message': 'File uploaded Successfully'}
        except Exception as ex:
            return {'message': str(ex)}
         

class ListFarmGeometryResource(Resource):
    # Adicionar customer_id futuramente
    def get(self, farm_id):
        area = areas.FarmAreaModel.find_by_id(farm_id)
        if area:            
            return area.as_json()
        return {'Message': 'area not found'}
