#  this file saves the scraped data from the website and
# caches the data as a json for future to avoid calling
# the network more than necessary.
from dataclasses import dataclass

import json
import os

from PokedexGUI.GlobalGUI import DEX_FOLDER

# check which generation the pokemon id falls in
GENERATIONS = [151, 251, 386, 493, 649, 721, 809, 905, 1025]



def check_data_availability(pokemon):
    # check if the requested pokemon has been registered in the database.
    # go through each gen directory and check the file names for a match.
    for generation in range(1, 10):  # generation 1-9
        path = f"{DEX_FOLDER}/gen_{generation}"
        # get the list of files in the directory
        files = os.listdir(path)
        # for each file in the directory, check if the name matches the pokemon
        for file in files:
            name = file.split(".")[0]
            if pokemon == name:
                # the pokemon is in the database!
                return generation

    return None

def attempt_pokemon_data_load(pokemon):
    pokemon = pokemon.title()
    generation = check_data_availability(pokemon)

    if not generation:
        return None

    # load the json for the pokemon data we have saved previously.
    dex_file = f"{DEX_FOLDER}/gen_{generation}/{pokemon}.json"
    with open(f"{dex_file}") as f:
        dex_data_json = json.load(f)
    return dex_data_json


@dataclass
class PokedexDataStorage:
    name: str
    dex_num: int
    genera: str
    artwork: list
    type: list
    capture_rate: int
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
        self.dex_data = self.get_data()

        generation = self.get_generation()
        pkmn_filename = f"{self.name}.json"
        filepath = f"{DEX_FOLDER}/gen_{generation}/{pkmn_filename}"

        self.generate_pokemon_file(filepath)
        self.save_pokemon_data(filepath, generation)

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

    # determine which generation the pokemon is from.
    def get_generation(self):
        gen_num = 1
        for gen in GENERATIONS:
            if self.dex_num <= gen:
                return gen_num
            else:
                gen_num += 1

    def get_data(self):
        return {
            "name": self.name,
            "dex_num": self.dex_num,
            "genera": self.genera,
            "artwork": self.artwork,
            "type": self.type,
            "capture_rate": self.capture_rate,
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
