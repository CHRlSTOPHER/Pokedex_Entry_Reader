from ParseWebpage import get_pkmn_api_data
from PokedexDataStorage import PokedexDataStorage
from PokedexGui import PokedexGui

HTTP_ERROR_MESSAGE = "Dex entry not found for "
LANGUAGE = "en"


class PokedexManager(PokedexGui):

    def __init__(self):
        PokedexGui.__init__(self)

        self.entry_value = None
        self.pkmn_data = None
        self.species_data = None

        # Dex Data
        self.name = None
        self.dex_num = None
        self.artwork = None
        self.type = []
        self.height = None
        self.weight = None
        self.abilities = []
        self.stats = []
        self.moves = []
        self.cries = {}
        self.flavour_text = []
        self.growth_rate = None
        self.egg_group = []

    def create_pokedex_entry(self, entry):
        entry_value = entry.widget.get()
        self.pkmn_data, self.species_data = get_pkmn_api_data(entry_value)

        # check if data was succesfully returned.
        if not self.pkmn_data and not self.species_data:
            print(f'{HTTP_ERROR_MESSAGE}"{self.entry_value}".')
            return

        self.name = entry_value.capitalize()
        self.dex_num = self.pkmn_data["id"]
        self.artwork = self.get_artwork()
        self.type = self.pkmn_data["types"]
        self.height = self.pkmn_data["height"]/10.0
        self.weight = self.pkmn_data["weight"]/10.0
        self.abilities = self.pkmn_data["abilities"]
        self.stats = self.pkmn_data["stats"]
        self.moves = self.pkmn_data["moves"]
        self.cries = self.pkmn_data["cries"]
        self.flavour_text = self.get_dex_flavor_text()

        self.growth_rate = self.species_data["growth_rate"]
        self.egg_group = self.species_data["egg_groups"]

        self.create_dex_entry_gui()

        # save the pokedex data for future use.
        data_storage = PokedexDataStorage(
            self.name, self.dex_num, self.artwork, self.type,
            self.height, self.weight, self.abilities, self.stats, self.moves,
            self.cries, self.flavour_text, self.growth_rate, self.egg_group
        )
        data_storage.save_json_data()

    def get_artwork(self):
        # store the pokemon artwork in a list
        official_artwork = self.pkmn_data["sprites"]["other"][('official'
                                                               '-artwork')]
        artwork_list = []
        for sprite in official_artwork:
            artwork = official_artwork[f"{sprite}"]
            artwork_list.append(artwork)
        return artwork_list

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
            language = language_dict['name']
            if language != LANGUAGE:
                continue  # don't add this entry

            version = entry['version']['name']
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
