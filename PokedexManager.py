from ParseWebpage import get_api_data
from PokedexDataStorage import (PokedexDataStorage,
                                attempt_pokemon_data_load)
from PokedexGUI.GuiFramework import GuiFramework

HTTP_ERROR_MESSAGE = "Dex entry not found for "
LANGUAGE = "en"

NAME = "name"
DEX_NUM = "dex_num"
GENERA = "genera"
ARTWORK = "artwork"
TYPE = "type"
CAPTURE = "capture_rate"
HEIGHT = "height"
WEIGHT = "weight"
ABILITIES = "abilities"
STATS = "stats"
MOVES = "moves"
CRIES = "cries"
FLAVOUR_TEXT = "flavour_text"
GROWTH_RATE = "growth_rate"
EGG_GROUP = "egg_group"
GENDER = "gender_rate"

POKEMON = "pokemon"
SPECIES = "pokemon-species"
STARTER = "bulbasaur"


class PokedexManager(GuiFramework):

    def __init__(self):
        # Dex Data
        GuiFramework.__init__(self)
        self.dex_entry = STARTER
        self.generation = None
        self.pkmn_data = None
        self.species_data = None
        self.name = None
        self.dex_num = 0
        self.genera = None
        self.artwork = []
        self.type = []
        self.height = 0
        self.weight = 0
        self.abilities = []
        self.stats = []
        self.moves = []
        self.cries = {}
        self.flavour_text = []
        self.growth_rate = {}
        self.egg_group = []
        self.gender_ratio = 0
        self.data_storage = None

        self.new_dex_entry(0)

        self.mainloop()

    def load_pokedex_data(self):
        # check if the entry already exists in our saved dex.
        dex_data = attempt_pokemon_data_load(self.dex_entry)

        # call the api if we do not already have the pokemon saved.
        if not dex_data:
            print(f"Loading Data for {self.dex_entry}...")
            self.pkmn_data = get_api_data(self.dex_entry, POKEMON)
            self.species_data = get_api_data(self.dex_entry, SPECIES)

        # verify that we have successfully retrieved the data.
        data_list = [dex_data, self.pkmn_data, self.species_data]
        has_data = self.verify_data(data_list)
        if not has_data:
            print(f'{HTTP_ERROR_MESSAGE}"{self.dex_entry}".')
            return

        # define the dex variables based on whether we have api data or not.
        if dex_data:
            self.define_dex_data(dex_data)
        else:
            self.define_api_data(self.dex_entry)

        # save the pokedex data for future use.
        self.data_storage = PokedexDataStorage(
            self.name, self.dex_num, self.genera, self.artwork, self.type,
            self.capture_rate, self.height, self.weight, self.abilities,
            self.stats, self.moves, self.cries, self.flavour_text,
            self.growth_rate, self.egg_group, self.gender_ratio
        )
        self.data_storage.save_json_data()
        self.generation = self.data_storage.get_generation()

        self.update_gui(self.data_storage, self.generation)

    def verify_data(self, data_list):
        data_bool = False
        for data in data_list:
            if data:
                data_bool = True

        return data_bool

    def define_dex_data(self, dex_data):
        self.name = dex_data.get(NAME)
        self.dex_num = dex_data.get(DEX_NUM)
        self.genera = dex_data.get(GENERA)
        self.artwork = dex_data.get(ARTWORK)
        self.type = dex_data.get(TYPE)
        self.capture_rate = dex_data.get(CAPTURE)
        self.height = dex_data.get(HEIGHT)
        self.weight = dex_data.get(WEIGHT)
        self.abilities = dex_data.get(ABILITIES)
        self.stats = dex_data.get(STATS)
        self.moves = dex_data.get(MOVES)
        self.cries = dex_data.get(CRIES)
        self.flavour_text = dex_data.get(FLAVOUR_TEXT)
        self.growth_rate = dex_data.get(GROWTH_RATE)
        self.egg_group = dex_data.get(EGG_GROUP)
        self.gender_ratio = dex_data.get(GENDER)

    def define_api_data(self, entry_value):
        self.name = entry_value.capitalize()
        self.dex_num = self.pkmn_data.get("id")
        self.genera = self.get_genera()
        self.artwork = self.get_artwork()
        self.type = self.pkmn_data.get("types")
        self.capture_rate = self.species_data.get(CAPTURE)
        self.height = self.pkmn_data.get(HEIGHT) / 10.0
        self.weight = self.pkmn_data.get(WEIGHT) / 10.0
        self.abilities = self.pkmn_data.get(ABILITIES)
        self.stats = self.pkmn_data.get(STATS)
        self.moves = self.pkmn_data.get(MOVES)
        self.cries = self.pkmn_data.get(CRIES)
        self.flavour_text = self.get_dex_flavor_text()
        self.growth_rate = self.species_data.get(GROWTH_RATE)
        self.egg_group = self.species_data.get("egg_groups")
        self.gender_ratio = self.species_data.get("gender_rate")

    def get_artwork(self):
        # store the pokemon artwork in a list
        official_artwork = self.pkmn_data["sprites"]["other"][('official'
                                                               '-artwork')]
        artwork_list = []
        for sprite in official_artwork:
            artwork = official_artwork[f"{sprite}"]
            artwork_list.append(artwork)
        return artwork_list

    def get_genera(self):
        genera = self.species_data.get(GENERA)
        for genus in genera:
            language = genus.get("language").get("name")
            if language == LANGUAGE:
                return genus.get("genus")

    def get_dex_flavor_text(self):
        # get the pokedex entries of the desired language
        dex_entries = self.species_data['flavor_text_entries']
        all_dex_entries = self.get_dex_language_entries(dex_entries)

        # ignore duplicate entries (ex: pkmn red & blue have the same entries)
        condensed_dex_entries = []
        for text in all_dex_entries.values():
            if text not in condensed_dex_entries:
                condensed_dex_entries.append(text)

        return condensed_dex_entries

    def get_dex_language_entries(self, dex_entries):
        flavour_text = {}
        # Get the dex entries of the desired language.
        for entry in dex_entries:
            language_dict = entry.get("language")
            language = language_dict[NAME]
            if language != LANGUAGE:
                continue  # don't add this entry

            version = entry['version'][NAME]
            # remove any hyphens. capitalize first letters.
            game_version = version.replace("-", " ")
            game_version = game_version.title()

            text = entry['flavor_text']
            # Remove \n and error values. Missingno???
            entry_text = text.replace("\n", " ").replace("", " ")
            flavour_text[game_version] = entry_text

        return flavour_text

    # debug
    def print_pokemon_data(self):
        print(
            f"Name: {self.name}\n"
            f"Dex Num: {self.dex_num}\n"
            f"Artwork: {self.artwork}\n"
            f"Type: {self.type}\n"
            f"Height: {self.height}\n"
            f"Weight: {self.weight}\n"
            f"Abilities: {self.abilities}\n"
            f"Stats: {self.stats}\n"
            f"Moves: {self.moves}\n"
            f"Cries: {self.cries}\n"
            f"Flavour Text: {self.flavour_text}\n"
            f"Growth Rate: {self.growth_rate}\n"
            f"Egg Group: {self.egg_group}"
        )


pokedex = PokedexManager()
