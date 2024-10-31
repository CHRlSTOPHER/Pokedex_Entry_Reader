import ttkbootstrap as tb

FONT = "Trebuchet MS"
FONT_SIZE = 13

ALT_EGG_GROUPS = {
    "ground": "Field",
    "indeterminate": "Amorphous",
    "plant": "Grass",
    "humanshape": "Human-Like",
    "water1": "Water 1",
    "water2": "Water 2",
    "water3": "Water 3",
    "no-eggs": "No Eggs"
}


class EggGroupGUI(tb.LabelFrame):

    def __init__(self, left_window):
        super().__init__(left_window, text=" Egg Group ",
                         padding=(0, -3, 0, -2),
                         style="frame.TLabelframe", labelanchor="n")
        self.grid(column=0, row=4, sticky="ew", columnspan=1, padx=(0, 2))
        self.generate()

    def generate(self):
        self.egg_label = tb.Label(self, font=(FONT, FONT_SIZE),
                                  style="frame.TLabel")
        self.egg_label.pack(pady=(0, 5))

    def update_egg_group(self, egg_groups):
        group_str = ""
        for egg_group in egg_groups:
            name = egg_group.get("name")
            if ALT_EGG_GROUPS.get(name):
                name = ALT_EGG_GROUPS.get(name)
            group_str += f" {name.title()} "

        self.egg_label.config(text=group_str)
