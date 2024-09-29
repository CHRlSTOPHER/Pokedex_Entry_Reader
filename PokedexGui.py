import io

from PIL import ImageTk, Image

import urllib.request

from tkinter import Tk
from tkinter import ttk as tk

WORDWRAP = 120


class PokedexGui:

    def __init__(self):
        self.pkmn_data = None
        self.species_data = None
        self.entry_value = None
        self.dex_text_label = None
        self.entry = None
        self.frame = None
        self.dex_img_label = None
        self.condensed_dex_entries = []
        self.artwork = []

        self.generate()

    def generate(self):
        # main frame
        root = Tk()
        self.frame = tk.Frame(root, padding=10)
        self.frame.grid()

        # pokemon name label and entry box
        tk.Label(self.frame, text="Choose a Pokemon").grid(column=0, row=0)
        tk.Entry(self.frame).grid(column=1, row=0, padx=5)
        root.bind("<Return>", self.create_pokedex_entry)

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
        reg_art, shiny_art = self.artwork
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
        parts = string.split(" ", n + 1)
        if len(parts) <= n + 1:
            return -1
        return len(string) - len(parts[-1]) - len(" ")

    def get_url_image(self, url):
        raw_data = urllib.request.urlopen(url).read()
        image = Image.open(io.BytesIO(raw_data))
        photo = ImageTk.PhotoImage(image)
        return photo