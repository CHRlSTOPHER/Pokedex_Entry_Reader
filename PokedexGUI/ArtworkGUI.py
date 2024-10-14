import ttkbootstrap as tb

import io

from PIL import ImageTk, Image

import urllib.request


ART_RES = 360


def create_art_frame(left_window):
    # Artwork PokedexGUI
    art_frame = tb.LabelFrame(left_window, text="ZAMN",
                              style="frame.TLabelframe")
    art_label = tb.Label(art_frame)
    art_frame.grid(column=0, row=0)
    art_label.pack()

    return art_frame, art_label


def load_artwork(artwork, art_label):
    # load url and apply it to the label widget.
    reg_art, shiny_art = artwork
    reg_img = get_url_image(reg_art)
    shiny_img = get_url_image(shiny_art)
    art_label.config(image=reg_img)
    art_label.image = reg_img


def load_artwork_description(data, art_frame):
    extra_zeros = ""
    if data.dex_num < 10:
        extra_zeros = "00"
    elif data.dex_num < 100:
        extra_zeros = "0"

    art_frame.config(text=f"   No.{extra_zeros}{data.dex_num}    "
                               f"     {data.name}   ")


def get_url_image(url):
    raw_data = urllib.request.urlopen(url).read()
    image = Image.open(io.BytesIO(raw_data))
    image = image.resize((ART_RES, ART_RES))
    photo = ImageTk.PhotoImage(image)
    return photo
