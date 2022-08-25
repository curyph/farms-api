import datetime
import os
from sentinelhub import SHConfig

import numpy as np


from sentinelhub import (
    CRS,
    BBox,
    DataCollection,
    DownloadRequest,
    MimeType,
    MosaickingOrder,
    SentinelHubDownloadClient,
    SentinelHubRequest,
    bbox_to_dimensions,
)

class SentinelImages(object):

    @classmethod
    def createSentinelInstance(cls):
        return cls()

    def start_process(self):
        betsiboka_coords_wgs84 = [-52.54, -13.08, -52.19, -12.68]

        resolution = 20
        betsiboka_bbox = BBox(bbox=betsiboka_coords_wgs84, crs=CRS.WGS84)
        betsiboka_size = bbox_to_dimensions(betsiboka_bbox, resolution=resolution)

        config = SHConfig()

        print(f"Image shape at {resolution} m resolution: {betsiboka_size} pixels")

        # evalscript_true_color = """
        #     //VERSION=3

        #     function setup() {
        #         return {
        #             input: [{
        #                 bands: ["B02", "B03", "B04"]
        #             }],
        #             output: {
        #                 bands: 3
        #             }
        #         };
        #     }

        #     function evaluatePixel(sample) {
        #         return [sample.B04, sample.B03, sample.B02];
        #     }
        # """

        # request_true_color = SentinelHubRequest(
        #     data_folder="test_dir",
        #     evalscript=evalscript_true_color,
        #     input_data=[
        #         SentinelHubRequest.input_data(
        #             data_collection=DataCollection.SENTINEL2_L2A,
        #             time_interval=("2020-06-12", "2020-06-13"),
        #         )
        #     ],
        #     responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
        #     bbox=betsiboka_bbox,
        #     size=betsiboka_size,
        #     config=config,
        # )

        # all_bands_response = request_true_color.save_data()
        return {'message': 'image downloaded'}