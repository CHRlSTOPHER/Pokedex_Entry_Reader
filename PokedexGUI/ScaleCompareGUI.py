import ttkbootstrap as tb
from PIL import ImageTk, Image
import urllib.request
import io

from PokedexGUI.GlobalGUI import BG_COLOR

TRAINER_IMG_PATH = "resources/icons/trainer-icon.png"

SCALE = 200
POKEMON_HEIGHT = SCALE
HUMAN_HEIGHT = SCALE
POKEMON_WIDTH = SCALE
HUMAN_WIDTH = SCALE

AVERAGE_HUMAN_SIZE = 1.7

class ScaleCompareGUI(tb.LabelFrame):

    def __init__(self, window):
        super().__init__(window, text="  Scale Comparison  ",
                         width=350, height=250,
                         style='frame.TLabelframe', labelanchor='n')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.grid(column=0, row=0)
        self.grid_propagate(False)  # freeze the frame size
        self.artwork = None

        self.generate()

    def generate(self):
        self.pokemon_canvas = tb.Label(self)
        self.pokemon_canvas.configure(background=BG_COLOR)

        self.human_canvas = tb.Label(self)
        self.human_canvas.configure(background=BG_COLOR)

    def load_scale_compare(self, pokemon_height, artwork):
        self.artwork = artwork
        pokemon_height = pokemon_height
        pokemon_scale = 1.0
        human_scale = 1.0

        if pokemon_height > AVERAGE_HUMAN_SIZE:
            human_scale = AVERAGE_HUMAN_SIZE / pokemon_height
        elif AVERAGE_HUMAN_SIZE > pokemon_height:
            pokemon_scale = pokemon_height / AVERAGE_HUMAN_SIZE

        p_height = POKEMON_HEIGHT * pokemon_scale
        p_width = POKEMON_WIDTH * pokemon_scale
        h_height = HUMAN_HEIGHT * human_scale
        h_width = HUMAN_WIDTH * human_scale

        # reset canvas
        self.pokemon_canvas.grid_forget()
        self.human_canvas.grid_forget()
        self.pokemon_canvas.grid(row=0, column=0, sticky='se', padx=(10, 10))
        self.human_canvas.grid(row=0, column=1, sticky='ws', padx=(10, 10))

        x_scale, y_scale = self.load_pokemon_photo(p_width, p_height)
        self.load_human_photo(h_width, h_height, x_scale, y_scale)

    def load_human_photo(self, width, height, x_scale, y_scale):
        # match the scale of the trainer with the pokemon's scale modifiers
        if x_scale != 1.0:
            width *= x_scale
            height *= x_scale
        elif y_scale != 1.0:
            width *= y_scale
            height *= y_scale

        # load canvas images
        image = Image.open(TRAINER_IMG_PATH)
        image = image.resize((int(width/2), int(height)))
        photo = ImageTk.PhotoImage(image)

        self.human_canvas.configure(image=photo)
        self.human_canvas.image = photo

    def load_pokemon_photo(self, width, height):
        reg_art, shiny_art = self.artwork
        raw_data = urllib.request.urlopen(reg_art).read()
        image = Image.open(io.BytesIO(raw_data))

        # Extract the alpha channel and threshold it at 200
        alpha = image.getchannel('A')
        alpha_thresh = alpha.point(lambda p: 255 if p > 200 else 0)

        # Make a new completely black image same size as original
        black_copy = Image.new('RGB', image.size)

        # Copy across the alpha channel from original
        black_copy.putalpha(alpha_thresh)

        bounding_box = image.getbbox()
        image = black_copy.crop(bounding_box)

        # preserve resolution ratio
        x_scale = 1.0
        y_scale = 1.0
        x, y = image.size
        if y > x:
            x_scale = x / y
        elif x > y:
            y_scale = y / x
        width *= x_scale
        height *= y_scale

        image = image.resize((int(width), int(height)))
        photo = ImageTk.PhotoImage(image)

        self.pokemon_canvas.configure(image=photo)
        self.pokemon_canvas.image = photo

        return x_scale, y_scale
