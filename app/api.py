from flask_restful import Api


def create_api(web_app):
    from app import resources
    api = Api(web_app)

    api.add_resource(resources.InitResource, '/api/init')
    api.add_resource(resources.HomeResource, '/api/home')
    api.add_resource(resources.SentinelResource, '/api/sentinel')
    api.add_resource(resources.FarmUploadResource, '/api/save-farm')
    api.add_resource(resources.ListFarmGeometryResource, '/api/farms/search')
    api.add_resource(resources.ListFarmReservesResource, '/api/farms/<int:farm_id>/reserves')
    api.add_resource(resources.ListStates, '/api/states')
    api.add_resource(resources.ListCities, '/api/states/<int:state_id>/cities')