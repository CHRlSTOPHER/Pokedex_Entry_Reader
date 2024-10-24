import ttkbootstrap as tb

FONT = "Trebuchet MS"
FONT_SIZE = 13


class GrowthRateGUI(tb.LabelFrame):

    def __init__(self, left_window):
        super().__init__(left_window, text=" Growth Rate ",
                         padding=(0, -2, 0, -2),
                         style="frame.TLabelframe", labelanchor="n")
        self.grid(column=1, row=1, sticky="ew", columnspan=1, padx=(5, 0))
        self.generate()

    def generate(self):
        self.growth_label = tb.Label(self, font=(FONT, FONT_SIZE),
                                     padding=(0, -1, 0, -1))
        self.growth_label.pack(pady=(1, 8))

    def update_growth_rate(self, growth_rate):
        growth = growth_rate.get("name").title()
        growth = growth.replace("-", " ")
        self.growth_label.config(text=growth)
