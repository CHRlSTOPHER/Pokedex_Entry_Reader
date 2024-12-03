import os

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
DEFAULT_LETTER = DEFAULT_POKEMON[0].upper()

class SearchGUI(tb.Frame):

    def __init__(self, window):
        super().__init__(window, style='frame.TFrame')
        self.grid(row=2, column=1, sticky='nsew', pady=(0, 15))

        self.search_label = None
        self.search_entry = None
        self.disable_load = True
        self.searches = []
        self.search_index = -1
        self.alphabet_list = []
        self.alphabet_dict = {}
        self.pokemon_letter_list = {}

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

        # name drop down value
        self.menu_name = StringVar()
        self.menu_name.set(DEFAULT_POKEMON)

        # trace_add function is in gui framework

        self.retrieve_database_names()

        # name drop down menu
        self.name_menu = tb.OptionMenu(self, self.menu_name, DEFAULT_POKEMON,
                                       self.pokemon_letter_list[DEFAULT_LETTER]
                                       )
        self.name_menu.grid(row=0, column=5)

        # letter drop down value
        self.menu_letter = StringVar()
        self.menu_letter.set(DEFAULT_LETTER)
        # this will bind a function to stringvar. updates trigger the function
        self.menu_letter.trace_add('write', self.update_name_menu)

        # letter drop down menu
        self.alphabet_menu = tb.OptionMenu(self, self.menu_letter,
                                           DEFAULT_LETTER, *self.alphabet_list)
        self.alphabet_menu.grid(row=0, column=4)


    def update_name_menu(self, *args):
        # don't set a new entry. we are only changing the menu values.
        self.disable_load = True

        # the user selected a new letter. change the options to match
        menu = self.name_menu["menu"]
        menu.delete(0, "end")
        if len(args) == 1:
            letter = args[0]
        else:
            letter = self.menu_letter.get()

        name_list = self.pokemon_letter_list[letter]
        self.name_menu.set_menu(name_list[0], *name_list)
        # re-enable
        self.disable_load = False

    def create_alphabet_collections(self):
        for letter in ALPHABET:
            letter = letter.upper()
            self.alphabet_list.append(letter)
            self.alphabet_dict[letter] = []
            self.pokemon_letter_list[letter] = []

    def append_to_search_list(self, query):
        # remove pokemon from search list if it already exists
        if query in self.searches:
            index = self.searches.index(query)
            self.searches.pop(index)
            self.search_index -= 1

        # add the query at the end of the list
        self.searches.append(query)
        self.search_index += 1
        if len(self.searches) > 1:
            self.left_button["state"] = ENABLED

    def retrieve_database_names(self):
        for generation in range(1, 10):  # generation 1-9
            path = f"{DEX_FOLDER}/gen_{generation}"
            # get all file names
            for file in os.listdir(path):
                # split the pokemon name from the file extension
                name = file.split(".")[0]
                # use the first letter to determine which key is assigned
                letter = name[0]
                # add the name to the dictionary's list
                # example: add Abra to the 'A' dictonary
                self.pokemon_letter_list[letter].append(name)

    def append_to_database_names(self, name):
        # if we acquire a new pokemon through an api call, append the name
        letter = name[0].upper()
        self.pokemon_letter_list[letter].append(name)
        self.update_name_menu(name)

    def get_menu_name(self):
        return self.menu_name

    def get_new_entry(self):
        return self.new_entry
