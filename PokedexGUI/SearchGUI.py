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

class SearchGUI(tb.Frame):

    def __init__(self, window):
        super().__init__(window, style='frame.TFrame')
        self.grid(row=2, column=1, sticky='nsew', pady=(0, 15))

        self.search_label = None
        self.search_entry = None
        self.searches = []
        self.search_index = -1
        self.alphabet = "abcdefghjijklmnopqrstuvwxyz"
        self.alphabet_dict = {}
        self.letter = 'b'

        self.generate()

    def generate(self):
        # equal column weight
        [self.columnconfigure(c, weight=1) for c in range(7)]
        self.rowconfigure(0, weight=1)

        # Move between Pokemon searches (left arrow - previous searches)
        # (right arrow - recent searches. right works after pressing left)
        self.left_button = tb.Button(self, text=' <', style='button.TButton')
        self.right_button = tb.Button(self, text=' >', style='button.TButton')
        self.left_button.grid(column=0, row=0, padx=(10, 0), sticky='w')
        self.right_button.grid(column=1, row=0, padx=(0, 5), sticky='w')
        self.left_button["state"] = DISABLED
        self.right_button["state"] = DISABLED

        # Search Label and Entry
        self.search_label = tb.Label(self, text="Search:",
                                     background=BG_COLOR, foreground=FG_COLOR,
                                     font=(FONT, FONT_SIZE, "bold"))
        self.search_label.grid(column=2, row=0, sticky='e', padx=(0, 3))

        self.search_entry = tb.Entry(self, width=12)
        self.search_entry.grid(sticky='w', row=0, column=3)

        # Alphabetical Dropdown menus


        self.create_alphabet_dict()

    def create_alphabet_dict(self):
        for letter in self.alphabet:
            self.alphabet_dict[letter] = []

    def append_to_search_list(self, query):
        self.searches.append(query)
        self.search_index += 1
        if len(self.searches) > 1:
            self.left_button["state"] = ENABLED
