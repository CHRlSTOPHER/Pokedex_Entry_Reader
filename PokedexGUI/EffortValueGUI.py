import ttkbootstrap as tb

FONT = "Trebuchet MS"
FONT_SIZE = 13
STAT_NAMES = ["HP", "ATK", "DEF", "SP ATK", "SP DEF", "SPD"]
STAT_DICT = {
    "hp": "HP",
    "attack": "ATK",
    "defense": "DEF",
    "special-attack": "SP ATK",
    "special-defense": "SP DEF",
    "speed": "SPD",
}

BLACK = "#373A3C"
FADED = "#C0C1C2"


class EffortValueGUI(tb.LabelFrame):

    def __init__(self, left_window):
        super().__init__(left_window, text=" Effort Values ", padding=(0, -5, 0, 0),
                         style="frame.TLabelframe", labelanchor="n")
        self.grid(row=5, column=0, columnspan=2, sticky="ew", pady=2)

        self.labels = []
        self.buttons = []

        self.generate()

    def generate(self):
        i = 0
        for stat in STAT_NAMES:
            label = tb.Label(self, text=stat, justify="center")
            label.grid(row=0, column=i)
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
                fg = BLACK
                text += f"{effort}"
            else:
                fg = FADED
                text += '0'

            label.config(text=text, foreground=fg)


            i += 1

        print(stats)