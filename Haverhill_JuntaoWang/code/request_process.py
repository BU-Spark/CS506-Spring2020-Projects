import pandas as pd
import string
import numpy as np
from folium import FeatureGroup, LayerControl, Map, Marker
from folium.plugins import MarkerCluster


class RequestProcess:
    def __init__(self, request_file_path: string):
        self.request_file_path = request_file_path

    def read_request(self):
        """
        read request from csv file and remove invalid entries
        :return:
        """
        # 0 = Request ID
        # 1 = Create Date
        # 5 = Status Code
        # 10 = Request Type ID
        # 11 = Request Type
        # 14 = Department ID
        # 15 = Department
        # 19 = Address
        # 28 = Priority
        # 29 = Longitude
        # 30 = Latitude
        requests = pd.read_csv(self.request_file_path, usecols=["Request ID", "Create Date", "Status Code",
                                                        "Request Type ID", "Request Type", "Department ID",
                                                        "Department", "Address", "Priority",
                                                        "Longitude", "Latitude"])
        request_valid = self.remove_invalid_entries(requests)

        return request_valid

    @staticmethod
    def remove_invalid_entries(requests: pd.DataFrame) -> pd.DataFrame:
        """
        remove all entries that do not have longitude or latitude
        :param requests:
        :return:
        """
        requests_position = np.array(requests[["Address", "Longitude", "Latitude"]])
        requests_drop = []
        for i in range(len(requests_position)):
            if requests_position[i][0] is np.nan or requests_position[i][1] == 0 or requests_position[i][2] == 0:
                requests_drop.append(i)
            elif str(requests_position[i][0]).find("`") != -1:
                requests_drop.append(i)
        requests_remain = requests.drop(requests_drop)
        requests_remain["Department"].fillna("Others", inplace=True)

        return requests_remain

    def classify_requests_coordinate(self, requests: pd.DataFrame) -> dict:
        """
        classify requests by type
        put same type of requests coordinates in a list
        requests_final = {Request Type: [[Latitude, Longitude, Address]]}
        :param requests:
        :return:
        """
        requests_type_dict = self.filter_request_type(requests)
        requests_final = {}
        for type_id in requests_type_dict:
            requests_final[requests_type_dict[type_id]] = []
        requests_type_coordinate = np.array(
            requests[["Request Type", "Latitude", "Longitude", "Address", "Department"]])
        for request in requests_type_coordinate:
            requests_final[request[4]].append([request[1], request[2], request[3], request[0]])

        return requests_final

    @staticmethod
    def filter_request_type(requests: pd.DataFrame):
        """
        find out all kinds of requests
        save request type in a dictionary: {Request Type ID: Request Type}
        :return:
        """
        requests_type = np.array(requests[["Department ID", "Department"]])
        requests_dict = {}
        for request in requests_type:
            request_id = request[0]
            if request_id not in requests_dict:
                requests_dict[request_id] = request[1]

        return requests_dict

    def get_final_requests(self) -> dict:
        requests = self.read_request()
        requests_final = self.classify_requests_coordinate(requests)

        return requests_final
