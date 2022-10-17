from flask_restful import Api


def create_api(web_app):
    from app import resources
    api = Api(web_app)

    # @web_app.route('/')
    # def index():
    #     return render_template('index.html')

    # @web_app.route('/', methods=['POST'])
    # def upload_file():
    #     uploaded_file = request.files['file']        
    #     print(uploaded_file)
    #     if uploaded_file.filename != '':
    #         uploaded_file.save(uploaded_file.filename)
    #     gpd.read_file('test.gpkg', layer='blocks')
    #     return redirect(url_for('index'))

    api.add_resource(resources.InitResource, '/api/init')
    api.add_resource(resources.HomeResource, '/api/home')
    api.add_resource(resources.SentinelResource, '/api/sentinel')
    api.add_resource(resources.FarmUploadResource, '/api/save-farm')
    api.add_resource(resources.ListFarmGeometryResource, '/api/farms/<int:farm_id>')
    api.add_resource(resources.ListFarmReservesResource, '/api/farms/<int:farm_id>/reserves')