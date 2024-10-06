import io

from PIL import ImageTk, Image

import urllib.request

from tkinter import BOTH
import tkinter as tk
# from tkinter import Toplevel
import ttkbootstrap as tb

WORDWRAP = 120
WINDOW_SIZE = "1280x720"
TITLE = "Pokedex Entries"
FONT = "courier"

DEBUG_WINDOW = "200x200+1452+216"
STARTER = "dragapult"
ART_RES = 330
ONE_TYPE_X = (115, 10)
TWO_TYPE_X = (65, 10)

TYPE_COLORS = {
    'fire': "E62829",
    'water': "2980EF",
    'grass': "3FA129",
    'steel': "60A1B8",
    'fairy': "EF70EF",
    'dragon': "5060E1",
    'fighting': "FF8000",
    'psychic': "EF4179",
    'dark': "624D4E",
    'bug': "91A119",
    'flying': "81B9EF",
    'electric': "FAC000",
    'ice': "3DCEF3",
    'ground': "915121",
    'rock': "AFA981",
    'normal': "9FA19F",
    'ghost': "704170",
    'poison': "9141CB",
}


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
        self.frame_label_style = None

        self.art_label = None
        self.art_frame = None
        self.type_1_label = None
        self.type_2_label = None

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
                                         font=(FONT, 15, 'bold'))
        self.frame_label_style.configure('frame.TLabelframe',
                                         borderwidth=4, relief="solid")

    def left_gui(self):
        self.left_window = tk.Frame(self, bg="black", padx=15, pady=10)
        self.left_window.grid(column=0, row=0)

        # Artwork GUI
        self.art_frame = tb.LabelFrame(self.left_window, text="ZAMN",
                                       style="frame.TLabelframe")
        self.art_label = tb.Label(self.art_frame)
        self.art_frame.grid(column=0, row=0)
        self.art_label.pack()

        # Type GUI
        self.type_frame = tb.LabelFrame(self.left_window, text="Type",
                                        style="frame.TLabelframe")

        self.type_frame.grid(column=0, row=1, sticky="NSEW", columnspan=100)
        self.type_1_label = tb.Label(self.type_frame, font=(FONT, 14, "bold"))
        self.type_2_label = tb.Label(self.type_frame, font=(FONT, 14, "bold"))
        self.type_1_label.grid(column=0, row=0, padx=TWO_TYPE_X, pady=(0, 10))
        self.type_2_label.grid(column=1, row=0, pady=(0, 10))

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
        self.update_types_labels(data.type)

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

    def update_types_labels(self, types):
        # reset text
        self.type_1_label.configure(text="")
        self.type_2_label.configure(text="")
        self.type_1_label.grid(padx=ONE_TYPE_X)
        if len(types) > 1:
            self.type_1_label.grid(padx=TWO_TYPE_X)

        i = 0
        labels = [self.type_1_label, self.type_2_label]
        for type in types:
            type = type.get("type").get('name')
            labels[i].configure(text=f"  {type.title()}  ",
                                foreground="white",
                                background=f"#{TYPE_COLORS.get(type)}")
            i += 1

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
