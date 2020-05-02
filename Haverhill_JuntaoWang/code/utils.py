import pyproj
import pandas as pd


def epsg3857_to_epsg4326(x: float, y: float) -> list:
    p1 = pyproj.Proj("epsg:3857")
    p2 = pyproj.Proj("epsg:4236")

    return pyproj.transform(p1, p2, x, y)


def extract_presentation_data():
    requests = pd.read_csv("resource/data/haverhill-request_updated.csv")
    requests = requests[0:5000]
    requests.to_csv("resource/data/haverhill-request_updated_presentation.csv")


if __name__ == '__main__':
    # x = -7913112.7619000003
    # y = 5280261.8451000005
    # res = epsg3857_to_epsg4326(x, y)
    # print(res)
    extract_presentation_data()
