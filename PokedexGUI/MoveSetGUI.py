import ttkbootstrap as tb

import math

from PokedexGUI.GlobalGUI import BG_COLOR, FG_COLOR

FRAME_HEIGHT = 500
FRAME_WIDTH = 310
HEIGHT = 270
WIDTH = 292
ROW_HEIGHT = 13.6
SCROLL_AMOUNT = -30

FONT = "Trebuchet MS"
FONT_SIZE = 12

VGD = 'version_group_details'
LLA = 'level_learned_at'
MLM = "move_learn_method"

LEARN_METHOD = {
    'tutor': "Move Tutor",
    'machine': "TM",
    'level-up': "Level Up"
}


class MoveSetGUI(tb.LabelFrame):

    def __init__(self, window):
        super().__init__(window, text="  Move Set  ",
                         style='frame.TLabelframe', labelanchor='n')

        self.grid(column=0, row=1, pady=(0, 4))
        self.config(width=FRAME_WIDTH, height=FRAME_HEIGHT)

        self.generate()

    def generate(self):
        self.canvas = tb.Canvas(self)
        self.canvas.configure(width=296, height=302)
        self.canvas.grid()
        self.canvas.configure(background=BG_COLOR)

        self.scrollbar = tb.Scrollbar(self)
        self.scrollbar.grid(sticky='ns', row=0, column=1, padx=(0, 4))
        self.scrollbar.rowconfigure(0, weight=1)
        self.scrollbar.columnconfigure(0, weight=1)
        self.scrollbar.config(command=self.canvas.yview)

        self.canvas.config(xscrollcommand=self.scrollbar.set,
                           yscrollcommand=self.scrollbar.set)
        self.canvas.bind("<MouseWheel>", self.scroll_event)

    def scroll_event(self, event):
        scroll = event.delta / SCROLL_AMOUNT
        self.canvas.yview_scroll(int(scroll), "units")

    def update_move_set(self, moves):
        # reset move set frame
        self.canvas.delete('all')

        # add all the move set labels to the canvas
        row = 0
        column = 0
        for move_data in moves:
            move_name = move_data.get('move').get('name')
            move_name = move_name.replace("-", " ").title()

            # column * x is the two possible column coordinates
            # + x is the base increase to the right for both
            x_position = (column * 135) + 80

            # row * y is the distance between each text and
            # + y is that little extra spacing at the start of the list
            # to push it into the labelframe instead of z-fighting it.
            y_position = (math.floor(row) * 24) + 16
            self.canvas.create_text(x_position, y_position, text=move_name,
                                    fill=FG_COLOR, font=(FONT, FONT_SIZE))

            row += 0.5
            column = (column + 1) % 2

        self.canvas.configure(scrollregion=(0, 0, 0, math.floor(row) * 24.6))
