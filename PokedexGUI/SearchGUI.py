from tkinter import StringVar

import ttkbootstrap as tb
from ttkbootstrap import DISABLED

from PokedexGUI.GlobalGUI import *

WORDWRAP = 120
WINDOW_SIZE = "1660x720"
TITLE = "Pokedex Entries"
FONT = "Trebuchet MS"
FONT_SIZE = 11
# button area size
AREA = 20
ENABLED = "normal"
ALPHABET = "abcdefghjijklmnopqrstuvwxyz"
DEFAULT_LETTER = 'B'

class SearchGUI(tb.Frame):

    def __init__(self, window):
        super().__init__(window, style='frame.TFrame')
        self.grid(row=2, column=1, sticky='nsew', pady=(0, 15))

        self.search_label = None
        self.search_entry = None
        self.searches = []
        self.search_index = -1
        self.alphabet_list = []
        self.alphabet_dict = {}
        self.letter = DEFAULT_LETTER

        self.generate()

    def generate(self):
        # equal column and row weight
        [self.columnconfigure(c, weight=1) for c in range(7)]
        self.rowconfigure(0, weight=1)

        self.generate_back_forward_gui()
        self.generate_search_gui()
        self.generate_drop_down_gui()

    def generate_back_forward_gui(self):
        # Move between Pokemon searches (left arrow - previous searches)
        # (right arrow - recent searches. right works after pressing left)
        self.left_button = tb.Button(self, text=' <', style='button.TButton')
        self.right_button = tb.Button(self, text=' >', style='button.TButton')
        self.left_button.grid(column=0, row=0, padx=(10, 0), sticky='w')
        self.right_button.grid(column=1, row=0, padx=(0, 0), sticky='w')
        self.left_button["state"] = DISABLED
        self.right_button["state"] = DISABLED

    def generate_search_gui(self):
        self.search_label = tb.Label(self, text="Search:",
                                     background=BG_COLOR, foreground=FG_COLOR,
                                     font=(FONT, FONT_SIZE, "bold"))
        self.search_label.grid(row=0, column=2, sticky='e', padx=(0, 3))

        self.search_entry = tb.Entry(self, width=12)
        self.search_entry.grid(row=0, column=3, sticky='w')

    def generate_drop_down_gui(self):
        self.create_alphabet_collections()

        # drop down gui
        letter = StringVar()
        letter.set(self.letter)
        self.alphabet_menu = tb.OptionMenu(self, letter, self.letter,
                                           *self.alphabet_list)
        self.alphabet_menu.grid(row=0, column=4)

    def create_alphabet_collections(self):
        for letter in ALPHABET:
            letter = letter.upper()
            self.alphabet_list.append(letter)
            self.alphabet_dict[letter] = []

    def append_to_search_list(self, query):
        self.searches.append(query)
        self.search_index += 1
        if len(self.searches) > 1:
            self.left_button["state"] = ENABLED
