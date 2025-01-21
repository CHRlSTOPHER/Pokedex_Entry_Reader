import ttkbootstrap as tb

WORDWRAP = 400
FONT = "Bahnschrift Light Condensed"
FONT = "Trebuchet MS"
FONT_SIZE = 16
X_PAD = 80
PAGE_NUM_SIZE = 20


class FlavourTextGUI(tb.LabelFrame):

    def __init__(self, window):
        super().__init__(window, text="  Pokedex Description  ",
                         width=562, height=370, padding=(0, -5, 0, 0),
                         style='frame.TLabelframe', labelanchor='n')
        self.grid(row=1, column=0, pady=(0, 10), columnspan=1, rowspan=2,
                  sticky='n')
        self.grid_propagate(False)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.page_number_label = None
        self.label = None
        self.entry = 1
        self.entry_total = 0
        self.descriptions = []

        self.generate()

    def generate(self):
        self.bind("<MouseWheel>", self.scroll_event)

        # displays the dex entry
        self.label = tb.Label(self, wraplength=WORDWRAP, justify="left",
                              style="frame.TLabel", font=(FONT, FONT_SIZE))
        self.label.grid(column=0, row=0, padx=(X_PAD, 0), pady=(30, 2),
                              sticky='w')
        self.label.bind("<MouseWheel>", self.scroll_event)

        self.page_number_label = tb.Label(self, style="frame.TLabel",
                                          font=(FONT, PAGE_NUM_SIZE))
        self.page_number_label.grid(sticky="se")

    def load_descriptions(self, descriptions):
        self.entry = 1
        self.entry_total = len(descriptions) - 1
        self.descriptions = descriptions

        # update page numbers and description
        self.page_number_label.config(text=f"1/{self.entry_total}")
        self.update_entries()

    def update_entries(self):
        text = self.descriptions[self.entry].replace("\u00ad ", "")
        self.label.configure(text=text)

    def scroll_event(self, event):
        direction = event.delta / -abs(event.delta)
        # validate page turn
        if self.entry + direction > self.entry_total:
            # exceeds max limit (overflow)
            self.entry = 1
        elif self.entry + direction == 0:
            # exceeds minimum limit (underflow)
            self.entry = self.entry_total
        else:
            self.entry += int(direction)

        self.page_number_label.config(text=f"{self.entry}/{self.entry_total}")
        self.update_entries()
