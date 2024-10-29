import ttkbootstrap as tb
from numpy.ma.core import minimum, maximum

CANVAS_WIDTH = 150
CANVAS_HEIGHT = 27

PINK = "#FF77DD"
BLUE = "#3355FF"

TEXT_X_1 = 21
TEXT_X_2 = 130

FONT = "Trebuchet MS"
FONT_SIZE = 12


class GenderGUI(tb.LabelFrame):

    def __init__(self, left_window):
        super().__init__(left_window, text = " Gender Ratio ",
                         style="frame.TLabelframe", labelanchor="n")
        self.grid(column=1, row=4, sticky='ew', columnspan=1, padx=(3, 0))
        self.columnconfigure(0, weight=1)

        self.gender_label = None
        self.gender_canvas = None

        self.generate()

    def generate(self):
        self.gender_label = tb.Label(self, text=" Gender Unknown ",
                                     padding = (0, -3, 0, 0), font=(FONT, FONT_SIZE))
        self.gender_canvas = tb.Canvas(self, bg="white",
                                       height=CANVAS_HEIGHT, width=CANVAS_WIDTH)

    def update_bar_ratio(self, ratio):
        # cleanup widgets
        self.gender_canvas.delete('all')

        self.gender_canvas.grid()
        self.draw_gender_bars(ratio)

    def draw_gender_bars(self, ratio):
        female_ratio = ratio / 8.0 * 100
        male_ratio = 100 - female_ratio

        ratio_list = []
        if male_ratio > 0:
            ratio_list.append([male_ratio, BLUE])
        if female_ratio > 0:
            ratio_list.append([female_ratio, PINK])

        # Gender is unknown. Return.
        if ratio == -1:
            self.gender_canvas.create_text(75, 10, text="Gender Unknown",
                                           font=(FONT, FONT_SIZE), fill="black")
            return

        minimum_width = 0
        # shrink keeps the graph centered but shrinks it the bigger the num
        padding = 48
        maximum_width = 56

        # x1 is starting x
        # x2 is ending x
        # y1 is starting y
        # y2 is ending y
        x1, y1, x2, y2 = padding, 0, padding, 20
        text_x = TEXT_X_1
        for percent, color in ratio_list:
            # convert the percent to max width
            width = percent * (maximum_width / 100)
            x2 += width

            self.gender_canvas.create_rectangle(
                x1, y1, x2, y2, fill=color, outline="black", width=1
            )

            self.gender_canvas.create_text(
                text_x, 10,
                text=f"{percent}%", font=(FONT, FONT_SIZE),
                fill="black"
            )
            x1 = x2
            text_x = TEXT_X_2
