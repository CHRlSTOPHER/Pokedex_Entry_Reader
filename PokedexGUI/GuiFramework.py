import tkinter as tk

from PokedexGUI.ArtworkGUI import *
from PokedexGUI.TypeGUI import *
from PokedexGUI.AbilityGUI import *

WORDWRAP = 120
WINDOW_SIZE = "1600x900"
TITLE = "Pokedex Entries"
FONT = "lucida console"
FONT_SIZE = 15

DEBUG_WINDOW = "200x200+1452+216"
STARTER = "dragapult"
ONE_TYPE_X = (115, 10)
TWO_TYPE_X = (65, 10)


class GuiFramework(tk.Tk):

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
                                         font=(FONT, FONT_SIZE))
        self.frame_label_style.configure('frame.TLabelframe',
                                         borderwidth=4, relief="solid")

    def left_gui(self):
        self.left_window = tk.Frame(self, bg="black", padx=15, pady=10)
        self.left_window.grid(column=0, row=0)

        self.art_frame, self.art_label = create_art_frame(self.left_window)
        self.type_frame = create_type_frame(self.left_window)
        self.ability_frame = create_ability_frame(self.left_window)

    def middle_gui(self):
        pass

    def right_gui(self):
        pass

    def update_gui(self, data):
        load_artwork(self.artwork, self.art_label)
        load_artwork_description(data, self.art_frame)

        self.type_1_label, self.type_2_label = update_types_labels(
            data.type, self.type_frame, self.type_1_label, self.type_2_label
        )

        load_ability_labels(self.ability_frame, data.abilities)
