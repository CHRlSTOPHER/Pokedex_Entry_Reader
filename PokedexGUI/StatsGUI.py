import ttkbootstrap as tb

STAT_NAMES = {
    "hp": "HP",
    "attack": "ATK",
    "defense": "DEF",
    "special-attack": "SPA",
    "special-defense": "SPD",
    "speed": "SPE",
}
STAT_COLOR = {
    "HP": "green",
    "ATK": "yellow",
    "DEF": "orange",
    "SPA": "blue",
    "SPD": "dark blue",
    "SPE": "purple"
}
CANVAS_HEIGHT = 300
CANVAS_WIDTH = 300

TEXT_X = 35
X_BAR_BEGIN_POS = 75
MAX_BAR_SIZE = .84
BAR_THICKNESS = 30
SPACING = 20
EXTRA_SPACE = 25

FONT = "Trebuchet MS"
FONT_SIZE = 11


class StatsGUI(tb.LabelFrame):

    def __init__(self, middle_window):
        super().__init__(middle_window, text=" Stats ",
                         style="frame.TLabelframe", labelanchor="n")
        self.stat_canvas = None

        self.grid(row=0)
        self.generate()

    def generate(self):
        self.stat_canvas = tb.Canvas(self, bg="white",
                                     height=CANVAS_HEIGHT, width=CANVAS_WIDTH)

    def load_bar_graphs(self, stats):
        # clean up all previous graphs and remake it
        self.stat_canvas.delete("all")
        self.stat_canvas.grid()

        row = 0
        for stat_dict in stats:
            stat_name = stat_dict.get("stat").get("name")
            stat_value = stat_dict.get("base_stat")
            abbreviation = STAT_NAMES.get(stat_name)

            self.draw_bar_graph(stat_value, abbreviation, row)
            row += 1

    def draw_bar_graph(self, value, abbreviation, row):
        # graphs values
        max = value * MAX_BAR_SIZE
        spacing = (SPACING * (row + 1)) + (EXTRA_SPACE * (row + 0))
        x1, y1 = X_BAR_BEGIN_POS, spacing
        x2, y2 = X_BAR_BEGIN_POS + max, spacing + BAR_THICKNESS

        color = STAT_COLOR.get(abbreviation)
        text = f"{abbreviation}: {value}"
        self.stat_canvas.create_rectangle(
            x1, y1, x2, y2, width = 1, fill=color,
        )
        self.stat_canvas.create_text(
            TEXT_X, y1 + (BAR_THICKNESS / 2), text=text,
            font=(FONT, FONT_SIZE, "bold"), justify="left"
        )
