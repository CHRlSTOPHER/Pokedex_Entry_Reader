import ttkbootstrap as tb

HIDDEN_COLOR = "#00ADAD"
FONT = "Trebuchet MS"
FONT_SIZE = 13

GRID_STICKY = {
    1: [""],
    2: ["", ""],
    3: ["e", "", "w"]
}


def create_ability_frame(left_window):
    ability_frame = tb.LabelFrame(left_window, text=" Abilities ",
                                  style="frame.TLabelframe")
    ability_frame.grid(column=0, row=2, sticky="ew")

    return ability_frame

def load_ability_labels(ability_frame, abilities):
    # reset column weight
    ability_frame.grid_columnconfigure(0, weight=0)
    ability_frame.grid_columnconfigure(1, weight=0)
    ability_frame.grid_columnconfigure(2, weight=0)

    ability_labels = []
    for ability in abilities:
        name = ability.get("ability").get("name")
        hidden = ability.get("is_hidden")
        slot = ability.get("slot")

        # Make the name more readable
        name = name.replace("-", " ")
        name = name.title()

        ability_label = tb.Label(ability_frame, text=name,
                                 font=(FONT, FONT_SIZE, "bold"))
        if hidden:
            ability_label.configure(foreground=HIDDEN_COLOR)

        ability_labels.append(ability_label)

    # handle the grid function based on how many abilities are present
    i = 0
    for label in ability_labels:
        amount = len(ability_labels)
        sticky = GRID_STICKY.get(amount)[i]
        label.grid(column=i, row=0, pady=(0, 7), sticky=sticky)
        # give weight to columns in use
        ability_frame.grid_columnconfigure(i, weight=1)
        i += 1
