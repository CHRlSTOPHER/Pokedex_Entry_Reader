import ttkbootstrap as tb
from PIL import ImageTk, Image, ImageOps
import urllib.request
import io

from PokedexGUI.GlobalGUI import BG_COLOR, DARK_MODE

TRAINER_IMG_PATH = "resources/icons/trainer-icon.png"

SCALE = 220
GRAY = 190

AVERAGE_HUMAN_SIZE = 1.7

class ScaleCompareGUI(tb.LabelFrame):

    def __init__(self, window):
        super().__init__(window, text="  Scale Comparison  ",
                         width=380, height=300,
                         style='frame.TLabelframe', labelanchor='n')
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.grid(column=1, row=1, columnspan=2, padx=(8, 0), sticky='n')
        self.grid_propagate(False)  # freeze the frame size
        self.artwork = None
        self.pokemon_height = 0

        self.generate()

    def generate(self):
        self.pokemon_canvas = tb.Label(self)
        self.pokemon_canvas.configure(background=BG_COLOR)

        self.human_canvas = tb.Label(self)
        self.human_canvas.configure(background=BG_COLOR)

        self.pokemon_canvas.grid(row=0, column=0, sticky='se', padx=(10, 10))
        self.human_canvas.grid(row=0, column=1, sticky='ws', padx=(10, 10))

    def update_scale_compare(self, pokemon_height, artwork):
        self.pokemon_height = pokemon_height
        human_image = Image.open(TRAINER_IMG_PATH)
        pokemon_image = self.load_pokemon_image(artwork)
        # make image completely black and invert colors if theme is dark mode
        human_image = self.silhouette_image(human_image)
        pokemon_image = self.silhouette_image(pokemon_image)

        human_image, pokemon_image = self.resize_images(human_image,
                                                        pokemon_image)
        self.render_images(human_image, pokemon_image)

    def load_pokemon_image(self, artwork):
        # Open the image
        reg_art, shiny_art = artwork
        raw_data = urllib.request.urlopen(reg_art).read()
        image = Image.open(io.BytesIO(raw_data))

        # remove any excess empty space from the sides of the image
        bounding_box = image.getbbox()
        pokemon_image = image.crop(bounding_box)

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

        sizes = [human_image_width, human_image_height,
                 pokemon_image_width, pokemon_image_height]
        i = 0
        # sometimes images are smaller than they should be. do one extra check.
        if max(sizes) < SCALE:
            # divide scale by the biggest number, ex: 180/90 would = 2x
            multiplier = SCALE / max(sizes)
            for size in sizes:
                sizes[i] = size * multiplier
                i += 1

        # Lastly, apply the new scale values to the images themselves
        human_image = human_image.resize((int(sizes[0]), int(sizes[1])),
                                          Image.Resampling.LANCZOS)
        pokemon_image = pokemon_image.resize((int(sizes[2]), int(sizes[3])),
                                              Image.Resampling.LANCZOS)

        return human_image, pokemon_image

    def render_images(self, human_image, pokemon_image):
        human_photo = ImageTk.PhotoImage(human_image)
        self.human_canvas.configure(image=human_photo)
        self.human_canvas.image = human_photo

        pokemon_photo = ImageTk.PhotoImage(pokemon_image)
        self.pokemon_canvas.configure(image=pokemon_photo)
        self.pokemon_canvas.image = pokemon_photo

    def silhouette_image(self, image):
        # get alpha data from image
        alpha = image.getchannel('A')
        # define the threshold
        alpha_thresh = alpha.point(lambda p: GRAY if p > 200 else 0)

        # we cannot invert in rgba mode, so we make a new image in rgb mode
        image = Image.new('RGB', image.size)
        if DARK_MODE:
            image = ImageOps.invert(image)

        # re-apply the alpha channel to the rgb image
        image.putalpha(alpha_thresh)

        return image
