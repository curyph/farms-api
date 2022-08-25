from sqlalchemy import create_engine
import os

class SqlAlchemyEngine(object):
    
    @classmethod
    def gpd_connect(cls):
        engine = create_engine(os.environ['DATABASE_URL'])
        return engine