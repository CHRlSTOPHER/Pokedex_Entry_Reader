import ttkbootstrap as tb

from PIL import Image, ImageTk, ImageFilter

SPRITE_PATH = "resources/sprites/gen_"
DEFAULT_NAME = "  Sprites  "
ALT_NAME = "  Alternate Art  "
ALT_PATH = "resources/alt-art/"

VERSION_PATHS = {
    1: ['red-green', 'red-blue', 'yellow'],
    2: ['silver', 'gold', 'crystal'],
    3: ['emerald', 'firered-leafgreen'],
    4: ['diamond-pearl', 'platinum', 'heartgold-soulsilver'],
    5: ['black-white']
}


class SpriteGUI(tb.LabelFrame):

    def __init__(self, window):
        super().__init__(window, text=DEFAULT_NAME, width=950, height=330,
                         style="frame.TLabelframe", labelanchor='n')
        self.grid(row=0, column=0, pady=3, columnspan=6)
        self.grid_propagate(False)
        self.generation = None
        self.dex_num = None
        self.shiny = False
        self.sprite_labels = []

        self.generate()

    def generate(self):
        for x in range(12):
            sprite_label = tb.Label(self, style='frame.TLabel')
            self.sprite_labels.append(sprite_label)

    def update_sprites(self, generation, dex_num, shiny):
        self.generation = generation
        self.dex_num = dex_num
        self.shiny = shiny

        # check if sprites are availble
        if self.generation in VERSION_PATHS:
            self.config(text=DEFAULT_NAME)
            sprite_paths = self.get_sprite_paths()
            self.load_sprites(sprite_paths)
        else:
            self.cleanup_labels()
            self.reset_widgets([])
            self.config(text=ALT_NAME)
            self.load_alt_art()

    def get_sprite_paths(self):
        sprite_paths = []
        gen = self.generation
        # cycle through gens until we hit gen 6 - the end of sprites
        while gen < 6:
            version_paths = VERSION_PATHS.get(gen)
            for version in version_paths:
                # validate sprite exists
                if not self.valid_sprite(version):
                    continue
                sprite_path = f"{SPRITE_PATH}{gen}/{version}/"
                if self.shiny and gen > 1:
                    sprite_path += "shiny/"
                sprite_path += f"{self.dex_num:04d}.png"
                sprite_paths.append(sprite_path)
            gen += 1

        return sprite_paths

    def load_sprites(self, sprite_paths):
        self.reset_widgets(sprite_paths)
        for label in self.sprite_labels:
            label.grid_forget()

        sprites = 1
        row = 0
        column = 0
        for path in sprite_paths:
            # create the sprite
            sprite_image = Image.open(path)
            sprite_image.convert("RGBA")
            # remove any excess empty space from the sides of the image
            bounding_box = sprite_image.getbbox()
            sprite_image = sprite_image.crop(bounding_box)
            # slightly increase size
            x, y = sprite_image.size
            scale_up = 2
            sprite_image = sprite_image.resize(
                (int(x * scale_up), int(y * scale_up)),
                Image.Resampling.NEAREST)
            sprite_photo = ImageTk.PhotoImage(sprite_image)

            # create a label for the sprite. makes positioning more automated.
            # a canvas would be more of a hassle to organize.
            sprite_label = self.sprite_labels[sprites - 1]
            sprite_label.configure(image=sprite_photo)
            sprite_label.image = sprite_photo

            # adjust the row and column weight of the sprite labelframe
            # to fit the needs of the current sprite amount.
            # can range anywhere between 1 and 12 sprites.
            length = len(sprite_paths)
            if sprites == int((length / 2) + 1) and length > 6:
                column = 0
                row = 1
            sprite_label.grid(column=column, row=row)

            column += 1
            sprites += 1

    def load_alt_art(self):
        path = f"{ALT_PATH}{self.dex_num:04d}.png"

        try:
            alt_art = Image.open(path)
        except:
            print(f"Alt art does not exist for Dex Entry No.{self.dex_num}.")
            return

        alt_art.convert("RGB")
        scale_up = 1.0
        x, y = alt_art.size[0] * scale_up, alt_art.size[1] * scale_up
        alt_art = alt_art.resize((int(x), int(y)),)
        alt_photo = ImageTk.PhotoImage(alt_art)

        alt_art_label = tb.Label(self, image=alt_photo)
        alt_art_label.grid(column=0, row=0, pady=(0, 5))
        alt_art_label.image = alt_photo
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.sprite_labels.append(alt_art_label)

    def valid_sprite(self, version):
        validity = True
        if version == 'firered-leafgreen' and self.generation != 1:
            validity = False
        return validity

    def reset_widgets(self, sprite_paths):
        # reset labelframe weights
        [self.columnconfigure(i, weight=0) for i in range(6)]
        [self.rowconfigure(i, weight=0) for i in range(2)]

        if self.generation > 5:
            return

        # apply new weights to labelframe
        if len(sprite_paths) > 6:
            columns = int(len(sprite_paths) / 2)
            [self.columnconfigure(i, weight=1) for i in range(columns)]
            [self.rowconfigure(i, weight=1) for i in range(2)]
        elif sprite_paths:
            columns = len(sprite_paths)
            [self.columnconfigure(i, weight=1) for i in range(columns)]
            self.rowconfigure(0, weight=1)

    def cleanup_labels(self):
        for label in self.sprite_labels:
            label.grid_forget()
