import tkinter as tk
import ttkbootstrap as tb

from PokedexGUI.FlavourTextGUI import FlavourTextGUI
from PokedexGUI.MoveSetGUI import MoveSetGUI
from PokedexGUI.GlobalGUI import *
from PokedexGUI.ArtworkGUI import ArtworkGUI
from PokedexGUI.EffortValueGUI import EffortValueGUI
from PokedexGUI.GenderGUI import GenderGUI
from PokedexGUI.ScaleCompareGUI import ScaleCompareGUI
from PokedexGUI.SpriteGUI import SpriteGUI
from PokedexGUI.StatsGUI import StatsGUI
from PokedexGUI.TypeGUI import TypeGUI
from PokedexGUI.AbilityGUI import AbilityGUI
from PokedexGUI.HeightWeightGUI import HeightWeightGUI
from PokedexGUI.GrowthRateGUI import GrowthRateGUI
from PokedexGUI.EggGroupGUI import EggGroupGUI

WORDWRAP = 120
WINDOW_SIZE = "1660x720"
TITLE = "Pokedex Entries"
FONT = "Trebuchet MS"
FONT_SIZE = 13

DEBUG_WINDOW = "200x200+1452+216"
ONE_TYPE_X = (115, 10)
TWO_TYPE_X = (65, 10)


class GuiFramework(tk.Tk):

    def __init__(self):
        super().__init__()

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
        self.shiny = False
        self.sprite_gui = None
        self.scale_gui = None
        self.move_set_gui = None
        self.stats_gui = None
        self.gender_gui = None
        self.effort_gui = None
        self.frame_style = None
        self.label_style = None
        self.left_window = None
        self.middle_window = None
        self.right_window = None
        self.debug_window = None

        self.generate()

    def generate(self):
        # self.debug_menu()
        self.geometry(WINDOW_SIZE)
        self.title(TITLE)
        self.resizable(width=False, height=False)

        self.generate_styles()

        self.left_gui()
        self.middle_gui()
        self.right_gui()

    def generate_styles(self):
        self.frame_label_style = tb.Style()
        self.frame_label_style.configure('frame.TLabelframe.Label',
                                         font=(FONT, FONT_SIZE, "bold"))
        self.frame_label_style.configure('frame.TLabelframe',
                                         borderwidth=4, relief="solid")
        self.frame_label_style.configure('frame.TLabelframe',
                                         background=BG_COLOR,
                                         foreground=FG_COLOR)
        self.frame_label_style.configure('frame.TLabelframe.Label',
                                         background=BG_COLOR,
                                         foreground=FG_COLOR)

        self.label_style = tb.Style()
        self.label_style.configure('frame.TLabel',
                                   background=BG_COLOR, foreground=FG_COLOR)
        self.label_style.configure('frame.TLabel.Label',
                                   background=BG_COLOR)

        self.frame_style = tb.Style()
        self.frame_style.configure('frame.TFrame',
                                   background=BG_COLOR, foreground=FG_COLOR)
        self.frame_style.configure('frame.TFrame.Frame',
                                   background=BG_COLOR, foreground=FG_COLOR)

        self.config(background=BG_COLOR)

    def left_gui(self):
        self.left_window = tb.Frame(self, style='frame.TFrame')
        self.left_window.grid(column=0, row=0, padx=(10, 0), pady=(5, 15))

        self.artwork_gui = ArtworkGUI(self.left_window)
        self.type_gui = TypeGUI(self.left_window)
        self.ability_gui = AbilityGUI(self.left_window)
        self.hweight_gui = HeightWeightGUI(self.left_window)
        self.growth_gui = GrowthRateGUI(self.left_window)
        self.egg_group_gui = EggGroupGUI(self.left_window)
        self.effort_gui = EffortValueGUI(self.left_window)
        self.gender_gui = GenderGUI(self.left_window)

    def middle_gui(self):
        self.middle_window = tb.Frame(self, style='frame.TFrame')
        self.middle_window.grid(column=1, row=0, padx=15, pady=(0, 2))

        self.stats_gui = StatsGUI(self.middle_window)
        self.move_set_gui = MoveSetGUI(self.middle_window)

    def right_gui(self):
        self.right_window = tb.Frame(self, style='frame.TFrame')
        self.right_window.grid(column=2, row=0,  pady=5)

        self.scale_gui = ScaleCompareGUI(self.right_window)
        self.sprite_gui = SpriteGUI(self.right_window)
        self.flavour_text_gui = FlavourTextGUI(self.right_window)

        self.search_label = tb.Label(self.right_window, text="Search:",
                                     background=BG_COLOR, foreground=FG_COLOR,
                                     font=(FONT, 11, "bold"))
        self.search_label.grid(row=2, column=1, padx=(0, 10), sticky='ne')
        self.search_gui = tb.Entry(self.right_window, width=12)
        self.search_gui.grid(sticky='nw', row=2, column=2)
        self.search_gui.bind("<Return>", self.load_pokedex_data)

    def update_gui(self, data, generation):
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
        self.stats_gui.update_bar_graphs(data.stats)
        self.move_set_gui.update_move_set(data.moves)

        # right window
        self.scale_gui.update_scale_compare(data.height, self.artwork)
        self.sprite_gui.update_sprites(generation, data.dex_num, self.shiny)

        # far right window
        '''e'''
