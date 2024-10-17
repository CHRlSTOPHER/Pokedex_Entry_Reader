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
                         style="frame.TLabelframe", labelanchor="n")
        self.grid(column=0, row=2, sticky="ew")
        self.ability_labels = []

    def load_labels(self, abilities):
        # reset column weight
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)

        # clean up prior ability labels
        for label in self.ability_labels:
            label.grid_forget()

        # create a new label for each ability
        for ability in abilities:
            name = ability.get("ability").get("name")
            hidden = ability.get("is_hidden")

            # Make the name more readable
            name = name.replace("-", " ")
            name = name.title()

            ability_label = tb.Label(self, text=name,
                                     font=(FONT, FONT_SIZE, "bold"))
            if hidden:
                ability_label.configure(foreground=HIDDEN_COLOR)

            self.ability_labels.append(ability_label)

        # handle the grid function based on how many abilities are present
        i = 0
        for label in self.ability_labels:
            amount = len(self.ability_labels)
            sticky = GRID_STICKY.get(amount)[i]
            label.grid(column=i, row=0, pady=(0, 7), sticky=sticky)

            # give weight to columns in use
            self.grid_columnconfigure(i, weight=1)
            i += 1
