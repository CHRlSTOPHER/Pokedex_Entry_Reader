#  this file saves the scraped data from the website and
# caches the data as a json for future to avoid calling
# the network more than necessary.
from dataclasses import dataclass

import json

# check which generation the pokemon id falls in
GENERATIONS = [151, 251, 386, 493, 649, 721, 809, 905, 1025]
DEX_FOLDER = "pokedex_entries"

# store flavour text, name, picture, pokedex id number, height,
# weight, ability, cry, type, stats

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
            "egg_group": self.egg_group
        }

        generation = self.get_generation()

        filename = f"{self.name}.json"
        filepath = f"{DEX_FOLDER}/gen_{generation}/{filename}"

        # create the file if it doesn't exist
        try:
            f = open(filepath, "x")
            f.write("{}")
            f.close()
        except:
            return  # File already exists

        f = open(filepath)
        file_data = json.load(f)

        file_data.update(self.dex_data)
        with open(filepath, "w") as f:
            json.dump(file_data, f, indent=2)

    def load_json_data(self):
        # does not work yet. just copy pasted code atm.
        with open(TRANSFORMS_JSON) as f:
            data = json.load(f)

        nodes, names = self.get_all_nodes()
        for node in nodes:
            node.set_pos_hpr_scale(*data[node.get_name()])

    # determine which generation the pokemon is from.
    def get_generation(self):
        gen_num = 1
        for gen in GENERATIONS:
            if self.dex_num <= gen:
                return gen_num
            else:
                gen_num += 1
