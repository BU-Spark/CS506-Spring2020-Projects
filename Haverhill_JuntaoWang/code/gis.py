from folium import Map, GeoJson, GeoJsonTooltip, FeatureGroup, Marker, LayerControl
from folium.plugins import MarkerCluster

from preprocess import PreProcess
from request_process import RequestProcess
import os
import time
import string


class GIS:
    def __init__(self):
        self.preprocess = PreProcess()
        self.CDBG_map = None
        self.precincts_wards_map = None

        self.directory_path = 'result'
        if not os.path.exists(self.directory_path):
            os.mkdir(self.directory_path)

        self.refuse_routes_directory_path = os.path.join(self.directory_path, 'refuse_routes')
        if not os.path.exists(self.refuse_routes_directory_path):
            os.mkdir(self.refuse_routes_directory_path)

    def get_directory_path(self):
        return self.directory_path

    def draw_CDBG_map(self):
        self.CDBG_map = Map(location=[42.795390191429625, -71.07516023514027], zoom_start=12)
        data = self.preprocess.get_CDBG_geometry_data()
        geo_json = GeoJson(
            data,
            style_function=lambda feature: {
                'fillColor': '#ffff00',
                'color': 'black',
                'weight': 1,
            },
            control=False
        )
        geo_json.add_to(self.CDBG_map)

    def draw_precincts_wards_map(self):
        self.precincts_wards_map = Map(location=[42.795390191429625, -71.07516023514027], zoom_start=12)
        data = self.preprocess.get_precincts_wards_geometry_data()
        for i in range(len(data)):
            ward_info = data[i]
            precincts = ward_info['data']
            for j in range(len(precincts)):
                precinct = precincts[j]
                geo_json = GeoJson(
                    data=precinct,
                    style_function=lambda feature: {
                        'fillColor': '#A9A9A9',
                        'color': 'black',
                        'weight': 1,
                    },
                    highlight_function=lambda feature: {
                        'fillColor': '#FFBFFF',
                        'color': 'yellow',
                        'weight': 2,
                    },
                    tooltip=GeoJsonTooltip(fields=['Precinct']),
                    control=False
                )
                geo_json.add_to(self.precincts_wards_map)

    def draw_refuse_routes_map(self, refuse_routes_file_path: string = 'resource/data/Hav_Refuse_Routes_WGS84'
                                                                       '/Hav_Refuse_Routes_WGS84.json'):
        geo_map = Map(location=[42.795390191429625, -71.07516023514027], zoom_start=12)
        data = self.preprocess.get_refuse_routes_data(refuse_routes_file_path)
        keys_pool = [
            'MONDAY - Red Week',
            'TUESDAY - Red Week',
            'WEDNESDAY - Red Week',
            'THURSDAY - Red Week',
            'FRIDAY - Red Week',
            'MONDAY - Blue Week',
            'TUESDAY - Blue Week',
            'WEDNESDAY - Blue Week',
            'THURSDAY - Blue Week',
            'FRIDAY - Blue Week',
            'MERCANTILE - Every Friday'
        ]

        for key in keys_pool:
            feature_group = FeatureGroup(name=key, show=True)
            if key.endswith('Red Week'):
                color = 'red'
            elif key.endswith('Blue Week'):
                color = 'blue'
            else:
                color = 'black'
            for each in data[key]:
                geo_json = GeoJson(
                    data=each,
                    style_function=lambda feature, color=color: {
                        'fillColor': '#A9A9A9',
                        'color': color,
                        'weight': 3,
                    },
                    highlight_function=lambda feature, color=color: {
                        'fillColor': '#FFBFFF',
                        'color': color,
                        'weight': 4,
                    },
                    tooltip=key,
                    overlay=True
                )
                geo_json.add_to(feature_group)
            feature_group.add_to(geo_map)
        LayerControl().add_to(geo_map)

        cur_time = time.strftime('%m_%d_%Y_%H_%M_%S', time.localtime())
        file_name = 'refuse_routes_{}.html'.format(cur_time)

        geo_map.save(os.path.join(self.refuse_routes_directory_path, file_name))

    @staticmethod
    def draw_heat_map(geo_map: Map, requests: dict):
        show = True
        requests_list = sorted(requests.items(), key=lambda item: item[0])
        for request_type in requests_list:
            if show:
                feature_group = FeatureGroup(name=request_type[0], show=True)
                show = False
            else:
                feature_group = FeatureGroup(name=request_type[0], show=False)
            mc = MarkerCluster()
            for request in request_type[1]:
                # print(request[2])
                popup_info = 'Request Type: \n' + request[3] + '\nAddress: ' + request[2]
                mc.add_child(Marker(location=[request[0], request[1]], popup=popup_info))
            mc.add_to(feature_group)
            feature_group.add_to(geo_map)

        LayerControl().add_to(geo_map)

    def process_requests(self, requests_file_path: string):
        self.draw_CDBG_map()
        self.draw_precincts_wards_map()

        request_process = RequestProcess(requests_file_path)
        request_final = request_process.get_final_requests()
        self.draw_heat_map(self.CDBG_map, request_final)
        self.draw_heat_map(self.precincts_wards_map, request_final)

        cur_time = time.strftime('%m_%d_%Y_%H_%M_%S', time.localtime())
        cur_directory_path = os.path.join(self.directory_path, cur_time)
        if not os.path.exists(cur_directory_path):
            os.mkdir(cur_directory_path)

        self.CDBG_map.save(os.path.join(cur_directory_path, 'CDBG_requests.html'))
        self.precincts_wards_map.save(os.path.join(cur_directory_path, 'precincts_wards_requests.html'))


if __name__ == '__main__':
    # requests_file_path = 'resource/data/haverhill-request_updated.csv'
    # gis = GIS()
    # gis.draw_refuse_routes_map()
    # gis.process_requests(requests_file_path)
    pass
