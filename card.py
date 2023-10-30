import arcade

FACE_DOWN_IMAGE = ":resources:images/cards/cardBack_blue4.png"

class Card(arcade.Sprite):
    """ Card sprite """

    def __init__(self, suit, value, scale=1):
        """ Card constructor """

        # Attributes for suit and value
        self.suit = suit
        self.value = value

        # Image to use for the sprite when face up
        self.image_file_name = f":resources:images/cards/card{self.suit}{self.value}.png"
        self.is_face_up = False

        # Call the parent
        super().__init__(FACE_DOWN_IMAGE, scale, hit_box_algorithm="None")

    # card face down
    def face_down(self):
        self.texture = arcade.load_texture(FACE_DOWN_IMAGE)
        self.is_face_up = False

    def face_up(self):
        self.texture = arcade.load_texture(self.image_file_name)
        self.is_face_up = True

    def is_face_down(self):
        """ Is this card face down? """
        return not self.is_face_up

    def get_color(self):
        """ Get the color of the card based on its suit. """
        if self.suit in ("Hearts", "Diamonds"):
            return "Red"
        else:
            return "Black"