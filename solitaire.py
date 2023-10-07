import arcade
import random # for shuffling cards

from card import Card

SCREEN_WIDTH = 1050
SCREEN_HEIGHT = 750
SCREEN_TITLE = "Solitaire"

# sizing
CARD_SCALE = 0.5

# size of cards
CARD_WIDTH = 135 * CARD_SCALE
CARD_HEIGHT = 180 * CARD_SCALE

# size of mat
MAT_PERCENT_OVERSIZE = 1.25
MAT_HEIGHT = int(CARD_HEIGHT * MAT_PERCENT_OVERSIZE)
MAT_WIDTH = int(CARD_WIDTH * MAT_PERCENT_OVERSIZE)

# Space between mats
VERTICAL_MARGIN_PERCENT = 0.10
HORIZONTAL_MARGIN_PERCENT = 0.10

# Top of the page but on the Y axe
TOP_Y = SCREEN_HEIGHT - MAT_HEIGHT / 2 - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# Middle of the page but on the Y axe
MIDDLE_Y = TOP_Y - MAT_HEIGHT - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# Bottom of the page but on the Y axe
BOTTOM_Y = MAT_HEIGHT / 2 + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# Left of the page but on the X axe
LEFT_X = MAT_WIDTH / 2 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# Middle of the page but on the X axe
MIDDLE_X = SCREEN_WIDTH / 4

# Right of the page but on the X axe
RIGHT_X = SCREEN_WIDTH - MAT_WIDTH / 2 - MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# How far apart each pile goes
X_SPACING = MAT_WIDTH + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# Card
CARD_VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]


class Solitaire(arcade.Window):

    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Stock list
        self.card_list = None

        arcade.set_background_color(arcade.color.AO)

        # This is the stock pile
        self.held_cards = None

        # This is the stock pile and makes the drag go back to it's original location if needed
        self.held_cards_original_position = None

        # Stock list with all the mats tha cards lay on.
        self.pile_mat_list = None

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # List of cards
        self.held_cards = []

        # This is the stock pile and makes the drag go back to it's original location if needed
        self.held_cards_original_position = []

        # ---  Create the mats the cards go on.

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        # Sprite list with all piles for dropping cards.

        self.dropping_pile_list: arcade.SpriteList = arcade.SpriteList()

        # This is the location for the talon and the stock
        # pile #0 is stock pile
        # pile #1 is talon

        self.create_stock_talon()
        # print(len(self.pile_mat_list))

        # This is the location for the Foundation
        # pile #2-5 is foundation
        self.create_foundation()
        # print(len(self.pile_mat_list))

        # This is the location for the Tableau
        # pile #6-12 is tableau
        self.create_tableau()
        # print(len(self.pile_mat_list))



        # Sprite list.
        self.card_list = arcade.SpriteList()

        self.shuffle_cards()  # Shuffle the cards when setting up the game.



    def create_stock_talon(self):
        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_SEA_GREEN)
        pile.position = LEFT_X, TOP_Y
        self.pile_mat_list.append(pile)
        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_SEA_GREEN)
        pile.position = LEFT_X + X_SPACING, TOP_Y
        self.pile_mat_list.append(pile)





    def create_tableau(self):
        for i in range(7):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_SEA_GREEN)
            pile.position = MIDDLE_X + i * X_SPACING, MIDDLE_Y
            self.pile_mat_list.append(pile)
            self.dropping_pile_list.append(pile)

    def create_foundation(self):
        for i in range(4):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_SEA_GREEN)
            pile.position = RIGHT_X - i * X_SPACING, TOP_Y
            self.pile_mat_list.append(pile)
            self.dropping_pile_list.append(pile)

    def shuffle_cards(self):
        """ Shuffle the card list. """
        # Create a new list for shuffling cards
        shuffled_card_list = []

        # Create card objects and add them to the shuffled list
        for card_suit in CARD_SUITS:
            for card_value in CARD_VALUES:
                card = Card(card_suit, card_value, CARD_SCALE)
                card.position = LEFT_X, TOP_Y
                shuffled_card_list.append(card)

        # Shuffle the cards in the shuffled list
        random.shuffle(shuffled_card_list)

        # Clear the existing card list and add shuffled cards to it
        self.card_list.clear()
        self.card_list.extend(shuffled_card_list)


    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()

        # Draw the mats the cards go on top
        self.pile_mat_list.draw()

        # Draw the cards
        self.card_list.draw()

    def pull_to_top(self, card: arcade.Sprite):
        # remove and append to the end
        if card in self.card_list:
            self.card_list.remove(card)
            # Append it to the end to ensure it's drawn last
            self.card_list.append(card)


    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when User presses the mouse button """
        #get cards that were clicked
        cards = arcade.get_sprites_at_point((x, y), self.card_list)

        # If cards are found
        if cards:
            # Select the top card
            primary_card = cards[-1]

            # Grab selected card and put it on its original position
            self.held_cards = [primary_card]
            self.held_cards_original_position = [self.held_cards[0].position]

            # Bring the card to the top of the rendering order
            self.pull_to_top(self.held_cards[0])



    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """ User moves mouse and drags the selected/held card """

        # If a card is clicked, then move it along the mouse
        for card in self.held_cards:
            card.center_x += dx
            card.center_y += dy

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        """ Called when user releases the mouse button """

        # If user releases, drop card
        if len(self.held_cards) == 0:
            return

        # check if the card is dropped on a mat
        # get the top card on the mat


        # Check if there is an overlapping sprite with the released sprite

        #right now, it only check piles. in the future, it should check the top cards of the piles.
        overlapping_sprite = self.get_overlapping_sprite(self.held_cards[0], self.dropping_pile_list)

        if overlapping_sprite:
            print(f"Overlapping sprite found: {overlapping_sprite}")
        else:
            print("No overlapping sprite found")

        # shows that no card is held
        self.held_cards = []

    # checks if the card is in the mat, or card on top of another card
    def check_overlap(self, sprite1, sprite2):
        """
        Check if two sprites overlap with an overlap ratio greater than 50%.

        Args:
            sprite1 (arcade.Sprite): The first sprite.
            sprite2 (arcade.Sprite): The second sprite.

        Returns:
            bool: True if the overlap ratio is greater than 50%, False otherwise.
        """
        # Get the bounding box of the first sprite
        left1 = sprite1.left
        right1 = sprite1.right
        top1 = sprite1.top
        bottom1 = sprite1.bottom

        # Get the bounding box of the second sprite
        left2 = sprite2.left
        right2 = sprite2.right
        top2 = sprite2.top
        bottom2 = sprite2.bottom

        # Calculate the overlap area
        overlap_width = max(0, min(right1, right2) - max(left1, left2))
        overlap_height = max(0, min(top1, top2) - max(bottom1, bottom2))
        overlap_area = overlap_width * overlap_height

        # Calculate the area of the smaller sprite
        min_area = min(sprite1.width * sprite1.height, sprite2.width * sprite2.height)

        # Calculate the overlap ratio
        overlap_ratio = overlap_area / min_area

        # Check if overlap ratio is greater than 0.5 (50%)
        if overlap_ratio > 0.5:
            return True

        return False


    # gets the overlapping sprite (assumming that only one sprite is overlapping over 50%)
    def get_overlapping_sprite(self, sprite1, sprite_list):
        """
        Get the sprite from sprite_list that overlaps with sprite1, if one exists.

        Args:
            sprite1 (arcade.Sprite): The sprite to check for overlap.
            sprite_list (arcade.SpriteList): The list of sprites to check against.

        Returns:
            arcade.Sprite or None: The overlapping sprite, or None if no overlap is found.
        """
        for sprite2 in sprite_list:
            if sprite2 != sprite1:
                if self.check_overlap(sprite1, sprite2):
                    return sprite2  # Return the overlapping sprite if found

        return None  # Return None if no overlap is found

def main():
    """ Main function """
    window = Solitaire()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
