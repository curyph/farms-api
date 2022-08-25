from sentinelhub import SHConfig
import os

config = SHConfig()

config.instance_id = os.environ['SENTINEL_INSTANCE_ID']
config.sh_client_id = os.environ['SENTINEL_CLIENT_ID']
config.sh_client_secret = os.environ['SENTINEL_CLIENT_SECRET']

config.save()

