from fiona.io import ZipMemoryFile
import geopandas as gpd
from app.domain.connections import SqlAlchemyEngine
from app.models.areas import FarmAreaModel, FarmReserveModel, FarmPedologyModel
from app.models.general_info import CitiesModel, StatesModel
from shapely.geometry.multipolygon import MultiPolygon
from shapely import wkt
from app.infrastructure.databases import db
from geoalchemy2 import WKTElement

class HandleUserInput():    
    from app.models.areas import FarmAreaModel
    
    def __init__(self, file, state_id, city_id):
        self.file = file
        self.gdf = None
        self.filename = ''    
        self.state_id = state_id
        self.city_id = city_id

    def process_file(self):          
        with ZipMemoryFile(self.file) as memfile:
            with memfile.open() as f:
                self.filename = f.name
                crs = f.crs
                self.gdf = gpd.GeoDataFrame.from_features(f, crs=crs)
        self._save_file_to_db()        

    def _save_file_to_db(self):
        processed_gdf = self.gdf.copy()
        processed_gdf = processed_gdf[['geometry']]
        epsg = processed_gdf.crs.to_epsg()
        areas = []
        for geom in processed_gdf.geometry:
            area = geom.area/10000
            if geom.geom_type == 'Polygon':
                polygon_geometry = wkt.loads(str(geom))
                geom = MultiPolygon([polygon_geometry])   
            farm_area = FarmAreaModel(
                nome_fazenda=self.filename,                 
                area=area, 
                geometry=WKTElement(geom, epsg), 
                state_id=self.state_id, 
                city_id=self.city_id)   
            db.session.add(farm_area)
            db.session.commit()   
        areas.append({'id': farm_area.farm_id, 'geom': geom})
        self.create_intersections(areas)
        self.pedology_intersections(areas)

    def create_intersections(self, areas):
        sql = "SELECT geometry FROM reserves"        
        engine = SqlAlchemyEngine.gpd_connect()
        reserves = gpd.read_postgis(sql, engine, geom_col='geometry')        
        for area in areas:
            df1 = gpd.GeoDataFrame({'geometry': area['geom']})
            intersection = gpd.overlay(df1, reserves, how='intersection', keep_geom_type=True)
            for geom in intersection.geometry:
                area_ha = geom.area/10000
                if geom.geom_type == 'Polygon':
                    polygon_geometry = wkt.loads(str(geom))
                    geom = MultiPolygon([polygon_geometry])      
                farm_reserve = FarmReserveModel(farm_id=area['id'], area=area_ha, area_type='APP', geometry=WKTElement(geom, 3857))
                db.session.add(farm_reserve)
                db.session.commit()     


    def pedology_intersections(self, areas):
        sql = "SELECT * FROM pedology"
        engine = SqlAlchemyEngine.gpd_connect()
        pedology = gpd.read_postgis(sql, engine, geom_col='geometry')    
        lt = []    
        dc = {}     
        for area in areas:
            df1 = gpd.GeoDataFrame({'geometry': area['geom']})
            intersection = gpd.overlay(df1, pedology, how='intersection', keep_geom_type=True)

            for att, values in intersection.iterrows(): 
                if values['geometry'].geom_type == 'Polygon':
                    polygon_geometry = wkt.loads(str(values['geometry']))
                    geom = MultiPolygon([polygon_geometry])
                    values['geometry'] = geom
                lt.append(values.to_dict())            
                print(values.to_dict())
            
            for item in lt:                
                farm_pedology = FarmPedologyModel(
                    ped_id=item['ped_id'], 
                    cod_symbol=item['cod_symbol'], 
                    legend=item['legend'],
                    order=item['order'],
                    suborder=item['suborder'],
                    color_pattern=None,
                    geometry=WKTElement(item['geometry'], 3857)
                )                
                db.session.add(farm_pedology)
                db.session.commit()    
        
      