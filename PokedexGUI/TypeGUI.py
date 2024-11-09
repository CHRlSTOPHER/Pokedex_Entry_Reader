import ttkbootstrap as tb

TYPE_COLORS = {
    'fire': "E62829",
    'water': "2980EF",
    'grass': "3FA129",
    'steel': "60A1B8",
    'fairy': "EF70EF",
    'dragon': "5060E1",
    'fighting': "FF8000",
    'psychic': "EF4179",
    'dark': "624D4E",
    'bug': "91A119",
    'flying': "81B9EF",
    'electric': "FAC000",
    'ice': "3DCEF3",
    'ground': "915121",
    'rock': "AFA981",
    'normal': "9FA19F",
    'ghost': "704170",
    'poison': "9141CB",
}

FONT = "Trebuchet MS"
FONT_SIZE = 13
X = 4
FRAME_PAD = 2


class TypeGUI(tb.LabelFrame):

    def __init__(self, left_window):
        super().__init__(left_window, text=" Types ", padding=(0, -2, 0, -2),
                         style="frame.TLabelframe", labelanchor="n")
        self.grid(column=0, row=1, sticky="ew", pady=FRAME_PAD, columnspan=1)

        self.type_1_label = None
        self.type_2_label = None

        self.generate()

    def generate(self):
        self.type_1_label = tb.Label(self, font=(FONT, FONT_SIZE, "bold"),
                                     padding=(0, -1, 0, -1))

        self.type_2_label = tb.Label(self, font=(FONT, FONT_SIZE, "bold"),
                                     padding=(0, -1, 0, -1))
        # there will always be at least 1 type, so first type will have weight
        self.grid_columnconfigure(0, weight=1)

    def update_labels(self, types):
        # include label type if the pokemon has a second type
        if len(types) > 1:
            # add second label and apply weight to it.
            self.type_2_label.grid(row=0, column=1, padx=(X, X), pady=(1, 8),
                                   sticky='nw')
            self.grid_columnconfigure(1, weight=1)
            self.type_1_label.grid(row=0, column=0, padx=(X, X), pady=(1, 8),
                                   sticky='ne')

        else:
            # hide second label and remove weight
            self.type_2_label.grid_forget()
            self.type_1_label.grid(row=0, column=0, padx=(X, X), pady=(1, 8),
                                   sticky='n')
            self.grid_columnconfigure(1, weight=0)

        # set the name and add the bg color based on the type
        i = 0
        labels = [self.type_1_label, self.type_2_label]
        for type in types:
            type = type.get("type").get('name')
            labels[i].configure(text=f" {type.title()} ", foreground="white",
                                background=f"#{TYPE_COLORS.get(type)}")
            i += 1
