import ttkbootstrap as tb


def create_ability_frame(left_window):
    ability_frame = tb.LabelFrame(left_window, text=" Abilities ",
                                  style="frame.TLabelframe")
    ability_frame.grid(column=0, row=2, sticky="ew")
    ability_frame.grid_columnconfigure(0, weight=1)
    ability_frame.grid_columnconfigure(1, weight=1)
    return ability_frame
