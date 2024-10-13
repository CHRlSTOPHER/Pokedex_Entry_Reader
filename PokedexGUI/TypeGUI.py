import ttkbootstrap as tb

TYPE_COLORS = {
    'fire': "E62829",
    'water': "2980EF",
    'grass': "3FA129",
    'steel': "60A1B8",
    'fairy': "EF70EF",
    'dragon': "5060E1",
    'fighting': "FF8000",
    'psychic': "EF4179",
    'dark': "624D4E",
    'bug': "91A119",
    'flying': "81B9EF",
    'electric': "FAC000",
    'ice': "3DCEF3",
    'ground': "915121",
    'rock': "AFA981",
    'normal': "9FA19F",
    'ghost': "704170",
    'poison': "9141CB",
}

FONT = "courier"
FONT_SIZE = 13


def create_type_frame(left_window):
    # Type PokedexGUI
    type_frame = tb.LabelFrame(left_window, text=" Type ",
                               style="frame.TLabelframe")
    type_frame.grid(column=0, row=1, sticky="ew")
    type_frame.grid_columnconfigure(0, weight=1)
    type_frame.grid_columnconfigure(1, weight=1)
    return type_frame


def update_types_labels(types, type_frame, type_1_label, type_2_label):
    # delete pre-existing labels.
    if type_1_label:
        type_1_label.grid_forget()
    if type_2_label:
        type_2_label.grid_forget()

    # generate new labels depending amount of types.
    Z = 6
    type_1_label = tb.Label(type_frame, font=(FONT, FONT_SIZE, "bold"))
    type_1_label.grid(row=0, column=0, padx=(Z, Z), pady=(0, 9), sticky='ne')

    if len(types) > 1:
        type_2_label = tb.Label(type_frame, font=(FONT, FONT_SIZE, "bold"))
        type_2_label.grid(row=0, column=1, padx=(Z, Z), pady=(0, 9),
                               sticky='nw')

    # set the name and add the bg color based on the type
    i = 0
    labels = [type_1_label, type_2_label]
    for type in types:
        type = type.get("type").get('name')
        labels[i].configure(text=f" {type.title()} ", foreground="white",
                            background=f"#{TYPE_COLORS.get(type)}")
        i += 1

    return type_1_label, type_2_label
