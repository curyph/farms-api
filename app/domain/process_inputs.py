from fiona.io import ZipMemoryFile
import geopandas as gpd
from app.domain.connections import SqlAlchemyEngine

class HandleUserInput():
    def __init__(self, file):
        self.file = file

    # @property
    # def file(self):
    #     return self.file

    # @file.setter
    # def file(self, value):
    #     self._file = value
    #     return self._file

    def save_file_to_db(self):  
        with ZipMemoryFile(self.file) as memfile:
            with memfile.open() as f:
                crs = f.crs
                gdf = gpd.GeoDataFrame.from_features(f, crs=crs)
                print(gdf.head())
        
        engine = SqlAlchemyEngine.gpd_connect()
        gdf.to_postgis("farm_areas", engine, if_exists='append')


