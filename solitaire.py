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

        # This is the location for the talon and the stock
        self.create_stock_talon()

        # This is the location for the Tableau
        self.create_tableau()

        # This is the location for the Foundation
        self.create_foundation()

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

    def create_foundation(self):
        for i in range(4):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_SEA_GREEN)
            pile.position = RIGHT_X - i * X_SPACING, TOP_Y
            self.pile_mat_list.append(pile)

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
        self.card_list.remove(card)
        self.card_list.append(card)

    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when User presses the mouse button """
        # retrieve card that user clicked
        cards = arcade.get_sprites_at_point((x, y), self.card_list)

        # checks if a card is clicked
        if len(cards) > 0:
            # gets the very top card
            primary_card = cards[-1]

            # All other cases, grab the face-up card we are clicking on
            self.held_cards = [primary_card]
            # Saves the position
            self.held_cards_original_position = [self.held_cards[0].position]
            # Put on top in drawing order
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

        # shows that no card is held
        self.held_cards = []

def main():
    """ Main function """
    window = Solitaire()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
