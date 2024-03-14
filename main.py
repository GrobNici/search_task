import sys
import io
import requests
import argparse
from PIL import Image


def get_spn(toponym):
    toponym_delta_1 = list(
        map(float, toponym["boundedBy"]["Envelope"]['lowerCorner'].split()))
    toponym_delta_2 = list(
        map(float, toponym["boundedBy"]["Envelope"]['upperCorner'].split()))
    delta_1 = str(abs(toponym_delta_1[0] - toponym_delta_2[0]))
    delta_2 = str(abs(toponym_delta_1[1] - toponym_delta_2[1]))
    return (delta_1, delta_2)


PATH = "http://geocode-maps.yandex.ru/1.x/"

parser = argparse.ArgumentParser()
parser.add_argument("address", type=str)
args = parser.parse_args()

params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": args.address,
    "format": "json"}

response = requests.get(PATH, params)

if not response:
    print(f"Ошибка! Код ошибки: {response.status_code}")
    sys.exit(1)

json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
toponym_coodrs = toponym["Point"]["pos"]
toponym_longitude, toponym_latitude = toponym_coodrs.split(" ")
delta_1, delta_2 = get_spn(toponym)

PATH = "http://static-maps.yandex.ru/1.x/"

params = {
    "ll": ",".join([toponym_longitude, toponym_latitude]),
    "spn": ",".join([delta_1, delta_2]),
    "l": "map",
    "pt": "{},pm2rdm".format(",".join([toponym_longitude, toponym_latitude]))
}

response = requests.get(PATH, params)
Image.open(io.BytesIO(response.content)).show()
