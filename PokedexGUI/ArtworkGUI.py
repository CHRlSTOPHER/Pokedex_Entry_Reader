import ttkbootstrap as tb
from tkinter import CENTER

import io

from PIL import ImageTk, Image

import urllib.request

ART_RES = 300
FONT = "Trebuchet MS"
FONT_SIZE = 11

def get_url_image(url):
    raw_data = urllib.request.urlopen(url).read()
    image = Image.open(io.BytesIO(raw_data))
    image = image.resize((ART_RES, ART_RES))
    photo = ImageTk.PhotoImage(image)
    return photo


class ArtworkGUI(tb.LabelFrame):

    def __init__(self, left_window):
        super().__init__(left_window, text="ZAMN", padding=(0, -9, 0, 0),
                         style="frame.TLabelframe", labelanchor="n")
        self.grid(column=0, row=0, pady=(3, 0), columnspan=2)

        self.left_window = left_window
        self.art_label = None
        self.generate_label()

    def generate_label(self):
        self.art_label = tb.Label(self, padding=(15, 5, 15, 15))
        self.genera_label = tb.Label(self)

        self.genera_label.grid(row=0)
        self.art_label.grid(row=1)

    def load_artwork(self, artwork):
        # load url and apply it to the label widget.
        reg_art, shiny_art = artwork
        reg_img = get_url_image(reg_art)
        shiny_img = get_url_image(shiny_art)
        self.art_label.config(image=reg_img)
        self.art_label.image = reg_img

    def load_artwork_description(self, data):
        extra_zeros = ""
        if data.dex_num < 10:
            extra_zeros = "00"
        elif data.dex_num < 100:
            extra_zeros = "0"

        dex_num = f"{extra_zeros}{data.dex_num}"
        self.config(text=f"  No.{dex_num}   {data.name}  ")
        self.genera_label.config(text=f"{data.genera}", font=(FONT, FONT_SIZE))
