import ttkbootstrap as tb


class FlavourTextGUI(tb.LabelFrame):

    def __init__(self, window):
        super().__init__(window, text="  Flavour Text  ",
                         width=562, height=370,
                         style='frame.TLabelframe', labelanchor='n')
        self.grid(row=1, column=0, pady=(0, 10), columnspan=1, rowspan=2,
                  sticky='n')
        self.grid_propagate(False)

        self.generate()

    def generate(self):
        self.placeholder_label = tb.Label(self)
        self.placeholder_label.grid()
