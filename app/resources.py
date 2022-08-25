from flask_restful import Resource
from app.collections.download_sentinel_hub import SentinelImages
from flask import request
from app.domain.process_inputs import HandleUserInput

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
        file = request.files['files[]']
        user_input = HandleUserInput(file)
        user_input.save_file_to_db()
        return 