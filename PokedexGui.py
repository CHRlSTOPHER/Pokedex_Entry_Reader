import io

from PIL import ImageTk, Image

import urllib.request

import tkinter as tk
# from tkinter import ttk
import ttkbootstrap as ttk

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
        self.load_window()
        self.load_entry()
        self.window.mainloop()

    def load_window(self):
        self.window = tk.Tk()
        self.frame = ttk.Frame(self.window, padding=10)
        self.frame.grid()

    def load_entry(self):
        ttk.Label(self.frame, text="Choose a Pokemon").grid(column=0, row=0)
        ttk.Entry(self.frame).grid(column=1, row=0, padx=5)
        self.window.bind("<Return>", self.create_pokedex_entry)

    def create_dex_entry_gui(self):
        self.load_descriptions()
        self.load_stats()
        self.load_moves()
        self.load_flavour_text()
        self.load_sprites()

    def load_descriptions(self):
        pass

    def load_stats(self):
        pass

    def load_moves(self):
        pass

    def load_flavour_text(self):
        pass

    def load_sprites(self):
        # load url and apply it to the label widget.
        reg_art, shiny_art = self.artwork
        reg_img = self.get_url_image(reg_art)
        # shiny_img = self.get_url_image(shiny_art)
        # self.dex_img_label = tk.Label(self.frame, image=reg_img)
        # self.dex_img_label.grid(column=1, row=1)
        # self.dex_img_label.image = reg_img

    def get_url_image(self, url):
        raw_data = urllib.request.urlopen(url).read()
        image = Image.open(io.BytesIO(raw_data))
        photo = ImageTk.PhotoImage(image)
        return photo
