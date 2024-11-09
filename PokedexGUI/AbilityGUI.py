import ttkbootstrap as tb

HIDDEN_COLOR = "#00ADAD"
FONT = "Trebuchet MS"
FONT_SIZE = 13

GRID_STICKY = {
    1: [""],
    2: ["", ""],
    3: ["e", "", "w"]
}


class AbilityGUI(tb.LabelFrame):

    def __init__(self, left_window):
        super().__init__(left_window, text=" Abilities ",
                         padding=(0, -3, 0, 0),
                         style="frame.TLabelframe", labelanchor="n")
        self.grid(column=0, row=2, sticky="ew", columnspan=2, pady=1)
        self.all_labels = []
        self.ability_labels = []

        self.generate()

    def generate(self):
        # There will always be at least one ability.
        label_1 = tb.Label(self)
        label_2 = tb.Label(self)
        label_3 = tb.Label(self)
        self.all_labels = [label_1, label_2, label_3]

    def load_labels(self, abilities):
        # reset column weight
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)

        # reset ability labels
        for label in self.ability_labels:
            label.grid_forget()
            label.configure(foreground="white")

        # create a new label for each ability
        i = 0
        self.ability_labels = []
        for ability in abilities:
            name = ability.get("ability").get("name")
            hidden = ability.get("is_hidden")

            # Make the name more readable
            name = name.replace("-", " ")
            name = name.title()

            ability_label = self.all_labels[i]
            ability_label.configure(text=name, font=(FONT, FONT_SIZE),
                                    style="frame.TLabel")
            if hidden:
                ability_label.configure(foreground=HIDDEN_COLOR)

            self.ability_labels.append(ability_label)
            i += 1

        # handle the grid function based on how many abilities are present
        i = 0
        for label in self.ability_labels:
            amount = len(self.ability_labels)
            sticky = GRID_STICKY.get(amount)[i]

            if i > 0:
                label.grid(column=i, row=0, padx=(2, 0), pady=(0, 7),
                           sticky=sticky)
            else:
                label.grid(column=i, row=0, pady=(0, 7), sticky=sticky)

            # give weight to columns in use
            self.grid_columnconfigure(i, weight=1)
            i += 1
