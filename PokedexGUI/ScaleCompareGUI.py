import ttkbootstrap as tb
from PIL import ImageTk, Image
import urllib.request
import io

from PokedexGUI.GlobalGUI import BG_COLOR

TRAINER_IMG_PATH = "resources/icons/trainer-icon.png"

SCALE = 200

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
        self.pokemon_height = 0

        self.generate()

    def generate(self):
        self.pokemon_canvas = tb.Label(self)
        self.pokemon_canvas.configure(background=BG_COLOR)

        self.human_canvas = tb.Label(self)
        self.human_canvas.configure(background=BG_COLOR)

    def load_scale_compare(self, pokemon_height, artwork):
        self.pokemon_height = pokemon_height
        self.reset_canvas()
        human_image = Image.open(TRAINER_IMG_PATH)
        pokemon_image = self.load_pokemon_image(artwork)
        human_image, pokemon_image = self.resize_images(human_image,
                                                        pokemon_image)
        self.render_images(human_image, pokemon_image)

    def reset_canvas(self):
        self.pokemon_canvas.grid_forget()
        self.human_canvas.grid_forget()
        self.pokemon_canvas.grid(row=0, column=0, sticky='se', padx=(10, 10))
        self.human_canvas.grid(row=0, column=1, sticky='ws', padx=(10, 10))

    def load_pokemon_image(self, artwork):
        # Open the image
        reg_art, shiny_art = artwork
        raw_data = urllib.request.urlopen(reg_art).read()
        image = Image.open(io.BytesIO(raw_data))

        # Extract the alpha channel and threshold it at 200
        alpha = image.getchannel('A')
        alpha_thresh = alpha.point(lambda p: 255 if p > 200 else 0)

        # Make a new completely black image same size as original
        silhouette = Image.new('RGB', image.size)

        # Copy across the alpha channel from original
        silhouette.putalpha(alpha_thresh)

        # remove any excess empty space from the sides of the image
        bounding_box = image.getbbox()
        pokemon_image = silhouette.crop(bounding_box)

        return pokemon_image

    def resize_images(self, human_image, pokemon_image):
        human_image_width, human_image_height = human_image.size
        pokemon_image_width, pokemon_image_height = pokemon_image.size

        # First, we make sure the human and pokemon are matching in height.
        divider = human_image_height / pokemon_image_height
        human_image_height /= divider
        human_image_width /= divider

        # Second, we get the scale ratio between them based on their height
        # the shorter entity will be scaled down.
        human_scale = 1.0
        pokemon_scale = 1.0
        if self.pokemon_height > AVERAGE_HUMAN_SIZE:
            human_scale = AVERAGE_HUMAN_SIZE / self.pokemon_height
        elif AVERAGE_HUMAN_SIZE > self.pokemon_height:
            pokemon_scale = self.pokemon_height / AVERAGE_HUMAN_SIZE

        # Third, scale them both down to fit in the labelframe
        # preserve the scale difference during this process
        # get the biggest length out of the two images
        max_length = max(human_image_width, human_image_height,
                         pokemon_image_width, pokemon_image_height)
        scale_down = SCALE / max_length

        # Third, apply the scales to the image resolutions
        human_image_width *= (human_scale * scale_down)
        human_image_height *= (human_scale * scale_down)
        pokemon_image_width *= (pokemon_scale * scale_down)
        pokemon_image_height *= (pokemon_scale * scale_down)

        # Lastly, apply the new scale values to the images themselves
        human_image = human_image.resize((int(human_image_width),
                                          int(human_image_height)))
        pokemon_image = pokemon_image.resize((int(pokemon_image_width),
                                              int(pokemon_image_height)))

        return human_image, pokemon_image

    def render_images(self, human_image, pokemon_image):
        human_photo = ImageTk.PhotoImage(human_image)
        self.human_canvas.configure(image=human_photo)
        self.human_canvas.image = human_photo

        pokemon_photo = ImageTk.PhotoImage(pokemon_image)
        self.pokemon_canvas.configure(image=pokemon_photo)
        self.pokemon_canvas.image = pokemon_photo
