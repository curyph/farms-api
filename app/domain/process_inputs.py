from fiona.io import ZipMemoryFile
import geopandas as gpd
from app.domain.connections import SqlAlchemyEngine
from app.models.areas import FarmAreaModel, FarmReserveModel
from shapely.geometry.multipolygon import MultiPolygon
from shapely import wkt
from app.infrastructure.databases import db
from geoalchemy2 import WKTElement

class HandleUserInput():    
    from app.models.areas import FarmAreaModel
    
    def __init__(self, file):
        self.file = file
        self.gdf = None
        self.filename = ''    

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
            farm_area = FarmAreaModel(nome_fazenda=self.filename, area=area, geometry=WKTElement(geom, epsg))   
        db.session.add(farm_area)
        db.session.commit()   
        areas.append({'id': farm_area.id, 'geom': geom})
        self.create_intersections(areas)

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

    #engine = SqlAlchemyEngine.gpd_connect()
    #gdf.to_postgis("farm_areas", engine, if_exists='append')

      