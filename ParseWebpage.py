from urllib.error import HTTPError
from urllib.request import Request, urlopen
import json

ADDRESS = "https://pokeapi.co/api/v2/{}/{}/"
HEADERS = {'User-Agent': 'Mozilla/5.0'}


def get_api_data(entry_value, resource):
    address = ADDRESS.format(resource, entry_value)
    request = Request(url=address, headers=HEADERS)

    try:
        raw_data = urlopen(request).read()
        data = json.loads(raw_data)

        return data

    except HTTPError as http:
        print(http)
        return None
