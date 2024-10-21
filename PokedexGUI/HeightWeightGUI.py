import ttkbootstrap as tb
import math

FONT = "Trebuchet MS"
FONT_SIZE = 13
FRAME_PAD = 2
INCHES = 39.46
POUNDS = 2.20462


class HeightWeightGUI:

    def __init__(self, left_window):
        self.height_frame = None
        self.weight_frame = None
        self.height_label = None
        self.weight_label = None

        self.generate(left_window)

    def generate(self, left_window):
        self.height_frame = tb.LabelFrame(left_window, text=" Height ",
                                          style="frame.TLabelframe",
                                          padding=(0, -3, 0, 0),
                                          labelanchor="n")
        self.weight_frame = tb.LabelFrame(left_window, text=" Weight ",
                                          style="frame.TLabelframe",
                                          padding=(0, -3, 0, 0),
                                          labelanchor="n")

        self.height_frame.grid(column=0, row=3, sticky="news",
                               padx=(0, 2), pady=FRAME_PAD)
        self.height_frame.grid_columnconfigure(0, weight=1)

        self.weight_frame.grid(column=1, row=3, sticky="news",
                               padx=(2.5, 0), pady=FRAME_PAD)
        self.weight_frame.grid_columnconfigure(0, weight=1)

        self.height_label = tb.Label(self.height_frame,
                                     font=(FONT, FONT_SIZE))
        self.weight_label = tb.Label(self.weight_frame,
                                     font=(FONT, FONT_SIZE))
        self.height_label.grid(pady=(0, 5))
        self.weight_label.grid(pady=(0, 5))

    def update_hweight(self, height, weight):
        # calculate the feet and inches based on the meters.
        meters = height
        inches = meters * INCHES
        feet = math.floor(inches / 12)
        remaining_inches = math.floor(inches - feet * 12)
        # add a zero in front if the remaining inches is less than 10
        if remaining_inches < 10:
            remaining_inches = f"0{remaining_inches}"

        height = f"{feet}\'{remaining_inches}\"   {meters} m"
        self.height_label.configure(text=height)


        # calculate the
        kilograms = weight
        pounds = round(weight * POUNDS, 1)
        weight = f"{pounds} lbs.   {kilograms} kg"
        self.weight_label.configure(text=weight)
