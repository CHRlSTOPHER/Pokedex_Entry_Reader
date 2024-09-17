import io

from PIL import ImageTk, Image

import urllib.request

from tkinter import Tk
from tkinter import ttk as tk

from ParseWebpage import get_pkmn_api_data

HTTP_ERROR_MESSAGE = "Dex entry not found for "
LANGUAGE = "en"
WORDWRAP = 120


class PokedexGui:

    def __init__(self):
        self.dex_text_label = None
        self.entry = None
        self.frame = None
        self.dex_img_label = None
        self.condensed_dex_entries = []
        self.artwork_list = []

        self.generate()

    def generate(self):
        # main frame
        root = Tk()
        self.frame = tk.Frame(root, padding=10)
        self.frame.grid()

        # pokemon name label and entry box
        tk.Label(self.frame, text="Choose a Pokemon").grid(column=0, row=0)
        tk.Entry(self.frame).grid(column=1, row=0, padx=5)
        root.bind("<Return>", self.create_pokdex_entry)

        # text for pokedex flavor text
        self.dex_text_label = tk.Label(self.frame, font=("Arial", 11))
        self.dex_text_label.grid(column=0, row=1, pady=25)

        root.mainloop()

    def create_dex_entry_gui(self):
        # set all the entry texts on the label
        entry_texts = self.prettify_entries()
        self.dex_text_label['text'] = entry_texts

        if self.dex_img_label:
            self.dex_img_label.destroy()

        # load url and apply it to the label widget.
        reg_art, shiny_art = self.artwork_list
        reg_img = self.get_url_image(reg_art)
        self.dex_img_label = tk.Label(self.frame, image=reg_img)
        self.dex_img_label.grid(column=1, row=1)
        self.dex_img_label.image = reg_img

    def prettify_entries(self):
        # construct text for tkinter label
        entry_texts = ""
        for entry in self.condensed_dex_entries:
            # check which entries are too long.
            if len(entry) > WORDWRAP:
                spaces = entry.count(" ")
                middle = round(spaces / 2)
                middle_index = self.find_nth(entry, middle)
                # insert a \n in the middle of the long sentence.
                entry = entry[:middle_index] + "\n" + entry[middle_index:]

            # space out the entries for readability
            entry_texts += entry + "\n\n"

        return entry_texts[:-2]

    def find_nth(self, string, n):
        parts = string.split(" ", n+1)
        if len(parts) <= n + 1:
            return -1
        return len(string) - len(parts[-1]) - len(" ")

    def get_url_image(self, url):
        raw_data = urllib.request.urlopen(url).read()
        image = Image.open(io.BytesIO(raw_data))
        photo = ImageTk.PhotoImage(image)
        return photo


class PokedexManager(PokedexGui):

    def __init__(self):
        PokedexGui.__init__(self)

        self.entry_value = None
        self.pkmn_data = None
        self.species_data = None
        self.artwork_list = None
        self.pokedex_entries = None

    def create_pokdex_entry(self, entry):
        self.pkmn_data, self.species_data = get_pkmn_api_data(entry)

        # check if data was succesfully returned.
        if not self.pkmn_data and not self.species_data:
            print(f'{HTTP_ERROR_MESSAGE}"{self.entry_value}".')
            return

        self.get_artwork()
        self.get_dex_flavor_text()
        self.create_dex_entry_gui()

    def get_artwork(self):
        # store the pokemon artwork in a list
        official_artwork = self.pkmn_data["sprites"]["other"][('official'
                                                               '-artwork')]
        self.artwork_list = []
        for sprite in official_artwork:
            artwork = official_artwork[f"{sprite}"]
            self.artwork_list.append(artwork)

    def get_dex_flavor_text(self):
        # get the pokdex entries of the desired language
        dex_entries = self.species_data['flavor_text_entries']
        self.pokedex_entries = {}

        self.get_dex_language_entries(dex_entries)

        # combine duplicate entries (ex: pkmn red & blue have the same entries)
        self.condensed_dex_entries = []
        for text in self.pokedex_entries.values():
            if text not in self.condensed_dex_entries:
                self.condensed_dex_entries.append(text)

    def get_dex_language_entries(self, dex_entries):
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
            self.pokedex_entries[game_version] = entry_text


pokedex = PokedexManager()
