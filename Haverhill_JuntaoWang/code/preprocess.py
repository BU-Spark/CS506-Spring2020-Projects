import geopandas as gpd
from operator import itemgetter
import json
from pyproj import _datadir, datadir


class PreProcess:
    def __init__(self):
        self.CDBG_file_path = 'resource/data/Hav_CDBG_Area_WGS84/Hav_CDBG_Area_WGS84.json'
        self.precincts_wards_file_path = 'resource/data/Hav_Precincts_Wards_WGS84/Hav_Precincts_Wards_WGS84.json'

    def get_CDBG_geometry_data(self) -> dict:
        gdf = gpd.read_file(self.CDBG_file_path)
        gdf = gdf.to_crs(epsg='4326')
        data = json.loads(gdf.to_json())['features'][0]['geometry']

        return data

    def get_precincts_wards_geometry_data(self) -> list:
        gdf = gpd.read_file(self.precincts_wards_file_path)
        gdf = gdf.to_crs(epsg='4326')
        data = json.loads(gdf.to_json())['features']
        data = self.get_latest_data(data)
        data = self.put_precincts_into_wards(data)

        return data

    def get_latest_data(self, data) -> list:
        return list(filter(lambda item: item['properties']['Map_Year'] == 2011, data))

    # group precincts by wards
    # return list[{ward: 1, data: [...]}, {ward: 2, data: [...]}...]
    def put_precincts_into_wards(self, data) -> list:
        new_data = []
        ward = {}
        for i in range(len(data)):
            data_i = data[i]
            ward_number = data_i['properties']['Ward']
            if ward_number not in ward:
                new_data.append({'ward': ward_number, 'data': [data_i]})
                ward[ward_number] = data_i
            else:
                for j in range(len(new_data)):
                    data_j = new_data[j]
                    if data_i['properties']['Ward'] == data_j['ward']:
                        data_j['data'].append(data_i)
                        break

        for i in range(len(new_data)):
            new_data[i]['data'].sort(key=lambda item: item['properties']['Precinct'])

        # sort by ward number
        new_data.sort(key=itemgetter('ward'))
        return new_data

    @staticmethod
    def get_refuse_routes_data(refuse_routes_file_path) -> dict:
        data = {}
        gdf = gpd.read_file(refuse_routes_file_path)
        gdf = gdf.to_crs(epsg='4326')
        raw_data = json.loads(gdf.to_json())['features']
        for each in raw_data:
            if each['properties']['Name'] not in data:
                data[each['properties']['Name']] = [each['geometry']]
            else:
                data[each['properties']['Name']].append(each['geometry'])

        return data


if __name__ == '__main__':
    PreProcess().get_refuse_routes_data("resource/data/Hav_Refuse_Routes_WGS84/Hav_Refuse_Routes_WGS84.json")
