import io

from PIL import ImageTk, Image

import urllib.request

import tkinter as tk
from tkinter import Toplevel
import ttkbootstrap as ttk

WORDWRAP = 120
WINDOW_SIZE = "1280x720"
DEBUG_WINDOW = "200x200+1452+216"
STARTER = "bulbasaur"
ART_RES = 360


class PokedexGui(tk.Tk):

    def __init__(self):
        super().__init__()
        self.pkmn_data = None
        self.species_data = None
        self.entry_value = None
        self.entry = None
        self.frame = None
        self.condensed_dex_entries = []
        self.artwork = []

        self.generate()

    def generate(self):
        # self.debug_menu()
        self.geometry(WINDOW_SIZE)
        self.load_window_gui()

        self.load_pokedex_data(STARTER)

        self.mainloop()

    def load_window_gui(self):
        self.left_window = tk.Frame(self)
        self.art_frame = ttk.LabelFrame(self.left_window)
        self.art_label = ttk.Label(self.art_frame)

        self.left_window.grid()
        self.art_frame.grid(column=0, row=0)
        self.art_label.grid()
        # self.frame = ttk.Frame(self, padding=10)
        # self.label_frame = ttk.LabelFrame(self, text="Themes")
        # ttk.Label(self.label_frame, text="Choose a Pokemon").grid(column=0,
        #                                                          row=0)

        # self.frame.grid()
        # self.label_frame.grid(column=4, row=0)
        # self.entry = ttk.Entry(self.label_frame).grid(column=1, row=0, padx=5)
        # self.bind("<Return>", self.load_pokedex_data)

    def update_gui(self):
        self.load_artwork()
        self.load_descriptions()
        self.load_stats()
        self.load_moves()
        self.load_flavour_text()
        self.load_sprites()

    def load_artwork(self):
        pass

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
        shiny_img = self.get_url_image(shiny_art)
        self.art_label.config(image=reg_img)
        self.art_label.image = reg_img

    def get_url_image(self, url):
        raw_data = urllib.request.urlopen(url).read()
        image = Image.open(io.BytesIO(raw_data))
        image = image.resize((ART_RES, ART_RES))
        photo = ImageTk.PhotoImage(image)
        return photo

    def debug_menu(self):
        self.debug_window = Toplevel()
        self.debug_window.geometry(DEBUG_WINDOW)
        self.debug_window.title("DEBUG")

        self.x_label = ttk.Label(self.debug_window, text="X")
        self.x_label.grid(column=0, row=0, padx=10)

        self.subtract_x_button = ttk.Button(self.debug_window, text="-")
        self.subtract_x_button.grid(column=1, row=0)

        self.x_num_label = ttk.Label(self.debug_window, text="0")
        self.x_num_label.grid(column=2, row=0, padx=10)

        self.add_x_button = ttk.Button(self.debug_window, text="+")
        self.add_x_button.grid(column=3, row=0)

