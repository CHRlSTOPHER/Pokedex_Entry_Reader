import ttkbootstrap as tb


class FlavourTextGUI(tb.LabelFrame):

    def __init__(self, window):
        super().__init__(window, text="  Flavour Text  ",
                         width=560, height=280,
                         style='frame.TLabelframe', labelanchor='n')
        self.grid(row=2, column=0, pady=(0, 6), columnspan=3)
        self.grid_propagate(False)

        self.generate()

    def generate(self):
        self.placeholder_label = tb.Label(self)
        self.placeholder_label.grid()
