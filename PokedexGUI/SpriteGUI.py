import ttkbootstrap as tb
from sympy.physics.paulialgebra import delta

SPRITE_PATH = "resources/sprites/gen_"

VERSION_PATHS = {
    1: ['red-green', 'red-blue', 'yellow'],
    2: ['silver', 'gold', 'crystal'],
    3: ['emerald', 'firered-leafgreen'],
    4: ['diamond-pearl', 'platinum', 'heartgold-soulsilver'],
    5: ['black-white']
}


class SpriteGUI(tb.LabelFrame):

    def __init__(self, window):
        super().__init__(window, text="  Sprites  ", width=330, height=200,
                         style="frame.TLabelframe", labelanchor='n')
        self.grid(row=1, column=0, pady=3)
        self.grid_propagate(False)
        self.generation = None
        self.dex_num = None
        self.shiny = False

        self.generate()

    def generate(self):
        self.default_label = tb.Label(self)
        self.default_label.grid()

    def update_sprites(self, generation, dex_num, shiny):
        self.generation = generation
        self.dex_num = dex_num
        self.shiny = shiny

        # check if sprites are availble
        sprite_paths = None
        if self.generation in VERSION_PATHS:
            sprite_paths = self.get_sprite_paths()
            self.load_sprites(sprite_paths)

    def get_sprite_paths(self):
        sprite_paths = []
        gen = self.generation
        # cycle through gens until we hit gen 6 - the end of sprites
        while gen < 6:
            version_paths = VERSION_PATHS.get(gen)
            for version in version_paths:
                sprite_path = f"{SPRITE_PATH}{gen}/{version}/"
                if self.shiny and gen > 1:
                    sprite_path += "shiny/"
                sprite_path += f"{self.dex_num:04d}.png"
                sprite_paths.append(sprite_path)
            gen += 1

        return sprite_paths

    def load_sprites(self, sprite_paths):
        print(sprite_paths)
