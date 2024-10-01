#  this file saves the scraped data from the website and
# caches the data as a json for future to avoid calling
# the network more than necessary.
from dataclasses import dataclass

import json

# check which generation the pokemon id falls in
GENERATIONS = [151, 251, 386, 493, 649, 721, 809, 905, 1025]
DEX_FOLDER = "pokedex_entries"
DEX_JSON = "pokedex_list"


def attempt_pokemon_data_load(pokemon):
    pokemon = pokemon.title()
    # check if desired pokemon has been registered in the dex.
    with open(f"{DEX_JSON}.json") as f:
        dex_json = json.load(f)
        if pokemon not in dex_json:
            return None

    # load the json for the pokemon data we have saved previously.
    gen = dex_json[pokemon]
    dex_file = f"{DEX_FOLDER}/gen_{gen}/{pokemon}.json"
    with open(f"{dex_file}") as f:
        dex_data_json = json.load(f)
    return dex_data_json


@dataclass
class PokedexDataStorage:
    name: str
    dex_num: int
    artwork: list
    type: list
    height: float
    weight: float
    abilities: list
    stats: list
    moves: list
    cries: dict
    flavour_text: list
    growth_rate: dict
    egg_group: list
    gender_ratio: int

    def save_json_data(self):
        self.dex_data = {
            "name": self.name,
            "dex_num": self.dex_num,
            "artwork": self.artwork,
            "type": self.type,
            "height": self.height,
            "weight": self.weight,
            "abilities": self.abilities,
            "stats": self.stats,
            "moves": self.moves,
            "cries": self.cries,
            "flavour_text": self.flavour_text,
            "growth_rate": self.growth_rate,
            "egg_group": self.egg_group,
            "gender_rate": self.gender_ratio
        }

        generation = self.get_generation()
        pkmn_filename = f"{self.name}.json"
        filepath = f"{DEX_FOLDER}/gen_{generation}/{pkmn_filename}"

        self.generate_pokemon_file(filepath)
        self.save_pokemon_data(filepath, generation)
        self.append_pokemon_to_dex_list(generation)

    def generate_pokemon_file(self, filepath):
        # create the file if it doesn't exist
        try:
            f = open(filepath, "x")
            f.write("{}")
            f.close()
        except FileExistsError as FEE:
            '''File exists. No need to print the error. We expect this.'''
            return  # File already exists

    def save_pokemon_data(self, filepath, generation):
        # open the pokemon json file
        dex_entry_file = open(filepath)
        file_data = json.load(dex_entry_file)
        dex_entry_file.close()

        # add and save the dex data into the file
        file_data.update(self.dex_data)
        with open(filepath, "w") as dex_entry_file:
            json.dump(file_data, dex_entry_file, indent=2)
        dex_entry_file.close()

    def append_pokemon_to_dex_list(self, generation):
        # add the pokemon + gen to the pokedex list json.
        dex_filepath = f"{DEX_JSON}.json"
        dex_file = open(dex_filepath)
        file_data = json.load(dex_file)
        file_data[self.name] = generation
        dex_file.close()

        with open(dex_filepath, "w") as dex_file:
            json.dump(file_data, dex_file, indent=2)
        dex_file.close()

    # determine which generation the pokemon is from.
    def get_generation(self):
        gen_num = 1
        for gen in GENERATIONS:
            if self.dex_num <= gen:
                return gen_num
            else:
                gen_num += 1
