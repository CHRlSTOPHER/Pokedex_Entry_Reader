import ttkbootstrap as tb

import io

from PIL import ImageTk, Image

import urllib.request

ART_RES = 360


class ArtworkGUI(tb.LabelFrame):

    def __init__(self, left_window):
        super().__init__(left_window, text="ZAMN",
                         style="frame.TLabelframe", labelanchor="n")
        self.grid(column=0, row=0)

        self.left_window = left_window
        self.art_label = None
        self.generate_label()

    def generate_label(self):
        self.art_label = tb.Label(self)
        self.art_label.pack()

    def load_artwork(self, artwork):
        # load url and apply it to the label widget.
        reg_art, shiny_art = artwork
        reg_img = self.get_url_image(reg_art)
        shiny_img = self.get_url_image(shiny_art)
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

    def get_url_image(self, url):
        raw_data = urllib.request.urlopen(url).read()
        image = Image.open(io.BytesIO(raw_data))
        image = image.resize((ART_RES, ART_RES))
        photo = ImageTk.PhotoImage(image)
        return photo
