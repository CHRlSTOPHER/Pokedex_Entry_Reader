import webbrowser

from ParseWebpage import get_pkmn_api_data

HTTP_ERROR_MESSAGE = "Dex entry not found for "
LANGUAGE = "en"


class PokeApiDataManager:

    def __init__(self):
        self.entry_value = None
        self.pkmn_data = None
        self.species_data = None
        self.artwork_list = None
        self.pokedex_entries = None

    def scrape_poki_api_data(self, entry):
        self.entry_value = entry.widget.get()
        self.pkmn_data, self.species_data = get_pkmn_api_data(self.entry_value)

        if not self.pkmn_data and not self.species_data:
            print(f'{HTTP_ERROR_MESSAGE}"{self.entry_value}".')
            return

        official_artwork = self.pkmn_data["sprites"]["other"][('official'
                                                               '-artwork')]
        self.artwork_list = []
        for sprite in official_artwork:
            artwork = official_artwork[f"{sprite}"]
            self.artwork_list.append(artwork)

        # get the pokdex entries of the desired language
        dex_entries = self.species_data['flavor_text_entries']
        self.pokedex_entries = {}
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
            self.pokedex_entries[game_version] = entry_text

        for entry in self.pokedex_entries:
            print(f"Pokemon {entry}: {self.pokedex_entries[entry]}")
