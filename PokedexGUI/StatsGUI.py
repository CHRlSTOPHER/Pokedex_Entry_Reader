import ttkbootstrap as tb
from gradpyent.gradient import Gradient

from PokedexGUI.GlobalGUI import BG_COLOR, FG_COLOR

STAT_NAMES = {
    "hp": "HP",
    "attack": "ATK",
    "defense": "DEF",
    "special-attack": "SPA",
    "special-defense": "SPD",
    "speed": "SPE",
}
STAT_COLOR = {
    "HP": ["2dc84d", "2DAEF8"],
    "ATK": ["f7ea48", "FFBF2A"],
    "DEF": ["ff7f41", "FF4FFF"],
    "SPA": ["e03c31", "FF0FFF"],
    "SPD": ["753bbd", "4D0FFF"],
    "SPE": ["147bd1", "00BFFF"]
}

LINE_WIDTH = 2
GRADIENT_START = 0
STAT_LIMITS = {
    "HP": 255,  # blissey
    "ATK": 190,  # mega mewtwo
    "DEF": 230,  # shuckle
    "SPA": 194,  # mega mewtwo
    "SPD": 230,  # shuckle
    "SPE": 180,  # deoxys
}

CANVAS_HEIGHT = 340
CANVAS_WIDTH = 310

TEXT_X = 40
X_BAR_BEGIN_POS = 80
MAX_BAR_SIZE = .84
BAR_THICKNESS = 25.0
SPACING = 22
EXTRA_SPACE = 30

FONT = "Trebuchet MS"
FONT_SIZE = 11


class StatsGUI(tb.LabelFrame):

    def __init__(self, middle_window):
        super().__init__(middle_window, text="  Stats  ",
                         padding=(0, 0, 0, 0),
                         style="frame.TLabelframe", labelanchor="n")
        self.stat_canvas = None

        self.grid(column=0, row=0, rowspan=1, pady=(0, 2))
        self.generate()

    def generate(self):
        self.stat_canvas = tb.Canvas(self, height=CANVAS_HEIGHT,
                                     width=CANVAS_WIDTH)
        self.stat_canvas.configure(bg=BG_COLOR)
        self.stat_canvas.grid()

    def update_bar_graphs(self, stats):
        # clean up all previous graphs and remake it
        self.stat_canvas.delete("all")

        row = 0
        for stat_dict in stats:
            stat_name = stat_dict.get("stat").get("name")
            stat_value = stat_dict.get("base_stat")
            abbreviation = STAT_NAMES.get(stat_name)

            self.draw_bar_graph(stat_value, abbreviation, row)
            row += 1

    def draw_bar_graph(self, value, abbreviation, row):
        # define the max size of the bar
        max = value * MAX_BAR_SIZE

        # define the spacing between each bar vertically
        spacing = (SPACING * (row + 1)) + (EXTRA_SPACE * (row + 0))

        # x1 is top left rectangle corner, y1 is top right corner
        x1, y1 = X_BAR_BEGIN_POS, spacing

        # x2 is bottom left rect corner, y2 is bottom right
        x2, y2 = X_BAR_BEGIN_POS + max, spacing + BAR_THICKNESS

        text = f"{abbreviation}: {value}"
        # background rectangle that provides the outline for the gradient bars
        self.stat_canvas.create_rectangle(x1, y1, x2, y2, width=LINE_WIDTH)

        # change x2 from max length to just fraction of the full bar
        # we plan on making many small rectangles to create the illusion
        # of one full bar with a color gradient
        increment = max / value
        x2 = x1 + increment
        start_color, end_color = STAT_COLOR.get(abbreviation)
        start_color, end_color = f"#{start_color}", f"#{end_color}"
        gradient_list = self.get_gradient_list(abbreviation,
                                               start_color, end_color)

        # create gradient bars based on stat value
        for num in range(value):
            color = gradient_list[num]
            self.stat_canvas.create_rectangle(
                x1, y1, x2, y2, fill=color, width=0
            )
            # start where we last left off
            x1 = x2
            # update end point of rectangle
            x2 += increment

        self.stat_canvas.create_text(
            TEXT_X, y1 + (BAR_THICKNESS / 2), text=text, fill=FG_COLOR,
            font=(FONT, FONT_SIZE, "bold"), justify="left"
        )

    def get_gradient_list(self, stat,
                          start_color="#FF0000", end_color="#0000FF"):
        # store a list of float values between 0 and 1
        input_list = []
        stat_range = STAT_LIMITS.get(stat) - GRADIENT_START
        for number in range(stat_range):
            input = number / stat_range
            input_list.append(input)

        # convert the float values to color values
        gradient = Gradient(
            gradient_start=start_color,
            gradient_end=end_color,
            opacity=1
        )
        gradient_list = gradient.get_gradient_series(series=input_list,
                                                     fmt="html")
        # only start gradient after a certain point
        for num in range(len(gradient_list)):
            if num < GRADIENT_START:
                gradient_list.insert(0, start_color)
            else:
                break

        return gradient_list
