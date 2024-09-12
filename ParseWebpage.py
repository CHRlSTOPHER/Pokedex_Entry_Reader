from urllib.error import HTTPError
from urllib.request import Request, urlopen
import json

ADDRESS = "https://pokeapi.co/api/v2/{}/{}/"
POKEMON = "pokemon"
SPECIES = "pokemon-species"
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_pkmn_api_data(entry_value):
    pkmn_address = ADDRESS.format(POKEMON, entry_value)
    species_address = ADDRESS.format(SPECIES, entry_value)

    pkmn_request = Request(url=pkmn_address, headers=HEADERS)
    species_request = Request(url=species_address, headers=HEADERS)

    try:
        pkmn_raw_data = urlopen(pkmn_request).read()
        species_raw_data = urlopen(species_request).read()

        pkmn_data = json.loads(pkmn_raw_data)
        species_data = json.loads(species_raw_data)

        return pkmn_data, species_data

    except HTTPError as http:
        print(http)
        return None, None
