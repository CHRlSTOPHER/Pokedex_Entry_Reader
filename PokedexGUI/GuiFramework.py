import tkinter as tk
import ttkbootstrap as tb

from PokedexGUI.ArtworkGUI import ArtworkGUI
from PokedexGUI.EffortValueGUI import EffortValueGUI
from PokedexGUI.GenderGUI import GenderGUI
from PokedexGUI.StatsGUI import StatsGUI
from PokedexGUI.TypeGUI import TypeGUI
from PokedexGUI.AbilityGUI import AbilityGUI
from PokedexGUI.HeightWeightGUI import HeightWeightGUI
from PokedexGUI.GrowthRateGUI import GrowthRateGUI
from PokedexGUI.EggGroupGUI import EggGroupGUI

WORDWRAP = 120
WINDOW_SIZE = "1280x720"
TITLE = "Pokedex Entries"
FONT = "Trebuchet MS"
FONT_SIZE = 13

DEBUG_WINDOW = "200x200+1452+216"
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

        self.artwork_gui = None
        self.type_gui = None
        self.ability_gui = None
        self.hweight_gui = None
        self.growth_gui = None
        self.egg_group_gui = None
        self.search_gui = None

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

    def generate_styles(self):
        self.frame_label_style = tb.Style()
        self.frame_label_style.theme_use("cosmo")
        self.frame_label_style.configure('frame.TLabelframe.Label',
                                         font=(FONT, FONT_SIZE, "bold"))
        self.frame_label_style.configure('frame.TLabelframe',
                                         borderwidth=4, relief="solid")

    def left_gui(self):
        self.left_window = tk.Frame(self, padx=15, pady=5)
        self.left_window.grid(column=0, row=0)

        self.artwork_gui = ArtworkGUI(self.left_window)
        self.type_gui = TypeGUI(self.left_window)
        self.ability_gui = AbilityGUI(self.left_window)
        self.hweight_gui = HeightWeightGUI(self.left_window)
        self.growth_gui = GrowthRateGUI(self.left_window)
        self.egg_group_gui = EggGroupGUI(self.left_window)
        self.effort_gui = EffortValueGUI(self.left_window)
        self.gender_gui = GenderGUI(self.left_window)

    def middle_gui(self):
        self.middle_window = tk.Frame(self, padx=15, pady=5)
        self.middle_window.grid(column=1, row=0)

        self.stats_gui = StatsGUI(self.middle_window)

    def right_gui(self):
        self.right_window = tk.Frame(self, pady=5)
        self.right_window.grid(column=2, row=0)

        self.search_gui = tb.Entry(self.right_window)
        self.search_gui.grid(sticky='nesw')
        self.search_gui.bind("<Return>", self.load_pokedex_data)

    def update_gui(self, data):
        # left window
        self.artwork_gui.load_artwork(self.artwork)
        self.artwork_gui.load_artwork_description(data)
        self.type_gui.update_labels(data.type)
        self.ability_gui.load_labels(data.abilities)
        self.hweight_gui.update_hweight(data.height, data.weight)
        self.growth_gui.update_growth_rate(data.growth_rate)
        self.egg_group_gui.update_egg_group(data.egg_group)
        self.effort_gui.update_values(data.stats)
        self.gender_gui.update_bar_ratio(data.gender_ratio)

        # middle window
        self.stats_gui.load_bar_graphs(data.stats)
