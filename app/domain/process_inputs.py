from fiona.io import ZipMemoryFile
import geopandas as gpd
from app.domain.connections import SqlAlchemyEngine
from app.models.areas import FarmAreaModel
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
        for geom_raw in processed_gdf.geometry:   
            area = geom_raw.area/10000
            if geom_raw.geom_type == 'Polygon':
                polygon_geometry = wkt.loads(str(geom_raw))
                geom_raw = MultiPolygon([polygon_geometry])
            farm_area = FarmAreaModel(nome_fazenda=self.filename, area=area, geometry=WKTElement(geom_raw, epsg))
            db.session.add(farm_area)
            db.session.commit()
            

    #engine = SqlAlchemyEngine.gpd_connect()
    #gdf.to_postgis("farm_areas", engine, if_exists='append')

      