import ttkbootstrap as tb

from PokedexGUI.GlobalGUI import FG_COLOR, DARK_MODE

FONT = "Trebuchet MS"
FONT_SIZE = 13
STAT_NAMES = ["HP", "ATK", "DEF", "SP ATK", "SP DEF", "SPEED"]
STAT_DICT = {
    "hp": "HP",
    "attack": "ATK",
    "defense": "DEF",
    "special-attack": "SP ATK",
    "special-defense": "SP DEF",
    "speed": "SPEED",
}

if DARK_MODE:
    FADED = "gray"
else:
    FADED = "#B0B2B3"


class EffortValueGUI(tb.LabelFrame):

    def __init__(self, left_window):
        super().__init__(left_window, text=" Effort Values ",
                         padding=(0, -5, 0, 0),
                         style="frame.TLabelframe", labelanchor="n")
        self.grid(row=5, column=0, columnspan=2, sticky="ew", pady=2)

        self.labels = []
        self.buttons = []

        self.generate()

    def generate(self):
        i = 0
        for stat in STAT_NAMES:
            label = tb.Label(self, text=stat, justify="center", padding=(7, 0),
                             style="frame.TLabel")
            label.grid(row=0, column=i, pady=(0, 2))
            label.config(font=(FONT, FONT_SIZE))

            self.labels.append(label)

            self.grid_columnconfigure(i, weight=1)
            i += 1

    def update_values(self, stats):
        # create a dict that assigns effort values to our naming convention
        new_pokemon_ev_dict = {}
        for stat in stats:
            effort = stat.get("effort")
            full_stat_name = stat.get("stat").get("name")
            stat_abbreviation = STAT_DICT.get(full_stat_name)
            new_pokemon_ev_dict[stat_abbreviation] = effort

        # we run through our list. this ensures the order is correct.
        i = 0
        for stat in STAT_NAMES:
            effort = new_pokemon_ev_dict.get(stat)
            label = self.labels[i]

            # draw attention to effort with 1+ values
            text = f"{stat}\n"
            if effort > 0:
                fg = FG_COLOR
                text += f"{effort}"
            else:
                fg = FADED
                text += '0'

            label.config(text=text, foreground=fg)
            i += 1
