import arcade

FACE_DOWN_IMAGE = ":resources:images/cards/cardBack_blue4.png"

class Card(arcade.Sprite):
    """ Card sprite """

    def __init__(self, suit, value, scale=1):
        """ Card constructor """

        # Attributes for suit and value
        self.suit = suit
        self.value = value
        #to keep track of the card if it has been on the foundation pile once
        self.was_at_foundation_once = False

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

    def get_value(self):
        """ Get the numerical value of the card. A is 1, J is 11, Q is 12, and K is 13. """
        if self.value == "A":
            return 1
        elif self.value in ("J", "Q", "K"):
            return 11 if self.value == "J" else 12 if self.value == "Q" else 13
        else:
            return int(self.value)

     # get suit
    def get_suit(self):
        return self.suit

    def set_was_at_foundation_once(self, was_at_foundation_once):
        self.was_at_foundation_once = was_at_foundation_once

    def get_was_at_foundation_once(self):
        return self.was_at_foundation_once