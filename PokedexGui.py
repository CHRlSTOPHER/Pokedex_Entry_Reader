import io

from PIL import ImageTk, Image

import urllib.request

import tkinter as tk
from tkinter import Toplevel
import ttkbootstrap as tb

WORDWRAP = 120
WINDOW_SIZE = "1280x720"
TITLE = "Pokedex Entries"
DEBUG_WINDOW = "200x200+1452+216"
STARTER = "bulbasaur"
ART_RES = 360


class PokedexGui(tk.Tk):

    def __init__(self):
        super().__init__()

        self.left_window = None
        self.middle_window = None
        self.right_window = None
        self.pkmn_data = None
        self.species_data = None
        self.entry_value = None
        self.entry = None
        self.frame = None
        self.condensed_dex_entries = []
        self.artwork = []
        self.art_label = None
        self.art_frame = None
        self.frame_label_style = None

        self.debug_window = None

        self.generate()

    def generate(self):
        # self.debug_menu()
        self.geometry(WINDOW_SIZE)
        self.title(TITLE)
        self.generate_styles()

        self.left_gui()
        self.middle_gui()
        self.right_gui()

        self.load_pokedex_data(STARTER)

        self.mainloop()

    def generate_styles(self):
        self.frame_label_style = tb.Style()
        self.frame_label_style.theme_use("cosmo")
        self.frame_label_style.configure('frame.TLabelframe.Label',
                                         font=('courier', 15, 'bold'))
        self.frame_label_style.configure('frame.TLabelframe',
                                         borderwidth=4, relief="solid")

    def left_gui(self):
        self.left_window = tk.Frame(self, bg="black", padx=15, pady=10)

        # Artwork GUI
        self.art_frame = tb.LabelFrame(self.left_window, text="ZAMN",
                                       style="frame.TLabelframe")
        self.art_label = tb.Label(self.art_frame)

        left_gui = [self.left_window, self.art_frame, self.art_label]
        [gui.grid() for gui in left_gui]

        # self.frame.grid()
        # self.label_frame.grid(column=4, row=0)
        # self.entry = tbk.Entry(self.label_frame).grid(column=1, row=0,
        #                                               padx=5)
        # self.bind("<Return>", self.load_pokedex_data)

    def middle_gui(self):
        pass

    def right_gui(self):
        pass

    def update_gui(self, data):
        self.load_artwork(data)
        self.load_descriptions(data)
        self.load_stats(data)
        self.load_moves(data)
        self.load_flavour_text(data)
        self.load_sprites(data)

    def load_artwork(self, data):
        # load url and apply it to the label widget.
        reg_art, shiny_art = self.artwork
        reg_img = self.get_url_image(reg_art)
        shiny_img = self.get_url_image(shiny_art)
        self.art_label.config(image=reg_img)
        self.art_label.image = reg_img

    def load_descriptions(self, data):
        extra_zeros = ""
        if data.dex_num < 10:
            extra_zeros = "00"
        elif data.dex_num < 100:
            extra_zeros = "0"

        self.art_frame.config(text=f"   No.{extra_zeros}{data.dex_num}  "
                                   f"     {data.name}   ")

    def load_stats(self, data):
        pass

    def load_moves(self, data):
        pass

    def load_flavour_text(self, data):
        pass

    def load_sprites(self, data):
        pass

    def get_url_image(self, url):
        raw_data = urllib.request.urlopen(url).read()
        image = Image.open(io.BytesIO(raw_data))
        image = image.resize((ART_RES, ART_RES))
        photo = ImageTk.PhotoImage(image)
        return photo

    def debug_menu(self):
        pass
        # self.debug_window = Toplevel()
        # self.debug_window.geometry(DEBUG_WINDOW)
        # self.debug_window.title("DEBUG")

        # self.x_label = tbk.Label(self.debug_window, text="X")
        # self.x_label.grid(column=0, row=0, padx=10)

        # self.subtract_x_button = tbk.Button(self.debug_window, text="-")
        # self.subtract_x_button.grid(column=1, row=0)

        # self.x_num_label = tbk.Label(self.debug_window, text="0")
        # self.x_num_label.grid(column=2, row=0, padx=10)

        # self.add_x_button = tbk.Button(self.debug_window, text="+")
        # self.add_x_button.grid(column=3, row=0)
