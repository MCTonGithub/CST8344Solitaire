from typing import Optional

import arcade
import random  # for shuffling cards
import time # for tracking time span when double-clicking a card

from card import Card

WINDOW_WIDTH = 1024
WINDOW_HEIGHT = int(WINDOW_WIDTH * 0.75)
SCREEN_TITLE = "Solitaire"

# sizing
CARD_SCALE = 0.55

# size of cards
CARD_WIDTH = int(135 * CARD_SCALE)
CARD_HEIGHT = int(180 * CARD_SCALE)

# size of mat
MAT_PERCENT_OVERSIZE = 1.23
MAT_HEIGHT = int(CARD_HEIGHT * MAT_PERCENT_OVERSIZE )
MAT_WIDTH = int(CARD_WIDTH * MAT_PERCENT_OVERSIZE )

# Space between mats
VERTICAL_MARGIN_PERCENT = 0.10
HORIZONTAL_MARGIN_PERCENT = 0.10

# Top of the page but on the Y axe
TOP_Y = WINDOW_HEIGHT - MAT_HEIGHT / 2 - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# Middle of the page but on the Y axe
MIDDLE_Y = TOP_Y - MAT_HEIGHT - MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# Bottom of the page but on the Y axe
BOTTOM_Y = MAT_HEIGHT / 2 + MAT_HEIGHT * VERTICAL_MARGIN_PERCENT

# Left of the page but on the X axe
LEFT_X = MAT_WIDTH / 2 + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# Middle of the page but on the X axe
MIDDLE_X = WINDOW_WIDTH / 4

# Right of the page but on the X axe
RIGHT_X = WINDOW_WIDTH - MAT_WIDTH / 2 - MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# How far apart each pile goes
X_SPACING = MAT_WIDTH + MAT_WIDTH * HORIZONTAL_MARGIN_PERCENT

# Card
CARD_VALUES = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
CARD_SUITS = ["Clubs", "Hearts", "Spades", "Diamonds"]

# If we fan out cards stacked on each other, how far apart to fan them?
CARD_VERTICAL_OFFSET = int(CARD_HEIGHT * CARD_SCALE * 0.4)

# Constant for piles
PILE_COUNT = 13
STOCK_PILE = 0
TALON_PILE = 1
TABLEAU_PILE_1 = 2
TABLEAU_PILE_2 = 3
TABLEAU_PILE_3 = 4
TABLEAU_PILE_4 = 5
TABLEAU_PILE_5 = 6
TABLEAU_PILE_6 = 7
TABLEAU_PILE_7 = 8
FOUNDATION_PILE_1 = 9
FOUNDATION_PILE_2 = 10
FOUNDATION_PILE_3 = 11
FOUNDATION_PILE_4 = 12


class Solitaire(arcade.Window):

    def __init__(self):
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, SCREEN_TITLE)

        # Pile list
        self.card_list = None  #: Optional[arcade.SpriteList]

        arcade.set_background_color(arcade.color.AO)

        # This cards that we want to drag
        self.held_cards = None

        # This sets an original location so that a card can go back to
        self.held_cards_original_position = None

        # Sprite list with all the mats that cards lay on.
        self.pile_mat_list = None

        # List of lists, each holds a pile of cards.
        self.piles = None

        #for tracking double clicking condition
        self.click_count = 0
        self.threshold_to_meet = 0

        # Flag to determine game mode (True for Classic, False for Vegas)
        self.game_mode_flag = True

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """

        # Cards that we are dragging
        # self.held_cards = [0]
        self.held_cards = []

        # This is the original location of a card we are moving
        self.held_cards_original_position = []

        # ---  Create the mats the cards go on.

        # Sprite list with all the mats tha cards lay on.
        self.pile_mat_list: arcade.SpriteList = arcade.SpriteList()

        # Mat square for the Stock
        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_SEA_GREEN)
        pile.position = LEFT_X, TOP_Y
        self.pile_mat_list.append(pile)

        # Mat square for the Talon
        pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_SEA_GREEN)
        pile.position = LEFT_X + X_SPACING, TOP_Y
        self.pile_mat_list.append(pile)

        # Mats for the Tableau
        for i in range(7):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_SEA_GREEN)
            pile.position = MIDDLE_X + i * X_SPACING, MIDDLE_Y
            self.pile_mat_list.append(pile)

        # Mats for the Foundation
        for i in range(4):
            pile = arcade.SpriteSolidColor(MAT_WIDTH, MAT_HEIGHT, arcade.csscolor.DARK_SEA_GREEN)
            pile.position = RIGHT_X - i * X_SPACING, TOP_Y
            self.pile_mat_list.append(pile)

        # --- Create, shuffle, and deal the cards

        # Sprite list.
        self.card_list = arcade.SpriteList()

        # Create every card
        for card_suit in CARD_SUITS:
            for card_value in CARD_VALUES:
                card = Card(card_suit, card_value, CARD_SCALE)
                card.position = LEFT_X, TOP_Y
                self.card_list.append(card)

        # shuffle the cards
        for pos1 in range(len(self.card_list)):
            pos2 = random.randrange(len(self.card_list))
            self.card_list.swap(pos1, pos2)

        # Array of lists
        self.piles = [[] for _ in range(PILE_COUNT)]

        # put all the cards in stock pile
        for card in self.card_list:
            self.piles[STOCK_PILE].append(card)

        # Move cards from the stock to the Tableau face down
        for pile_no in range(TABLEAU_PILE_1, TABLEAU_PILE_7 + 1):
            # Deal number of cards that we want
            for j in range(pile_no - TABLEAU_PILE_1 + 1):
                # Take the card from the stock
                card = self.piles[STOCK_PILE].pop()
                # Put in the foundation pile
                self.piles[pile_no].append(card)
                # move the card to the pile we just created
                card.position = self.pile_mat_list[pile_no].position
                # put on top
                self.pull_to_top(card)

        # Flip top of the card in the foundation pile
        for i in range(TABLEAU_PILE_1, TABLEAU_PILE_7 + 1):
            self.piles[i][-1].face_up()

    def on_draw(self):
        """ Render the screen. """
        # Clear the screen
        self.clear()

        # Draw the mats the cards go on top
        self.pile_mat_list.draw()

        # Draw the cards
        self.card_list.draw()

        # Draw the game mode text
        mode_text = "Classic Mode" if self.game_mode_flag else "Vegas Mode"
        arcade.draw_text(mode_text, 10, 10, arcade.color.WHITE, 14)

    def pull_to_top(self, card: arcade.Sprite):

        # remove and append to the end
        self.card_list.remove(card)
        self.card_list.append(card)



    def on_mouse_press(self, x, y, button, key_modifiers):
        """ Called when User presses the mouse button """

        first_clicked = time.time() % 60 #converts to seconds in minute, than seconds in day

        # get cards that were clicked
        cards = arcade.get_sprites_at_point((x, y), self.card_list)

        # Get mats that were clicked
        mats = arcade.get_sprites_at_point((x, y), self.pile_mat_list)

        # If click on a card
        if len(cards) > 0:

            # Select the top card
            primary_card = cards[-1]
            assert isinstance(primary_card, Card)

            # Check which pile the card is from
            pile_index = self.get_pile_for_card(primary_card)
            print(pile_index, "pile index")

            #tracks if card sprite is clicked twice or not
            if (first_clicked -  self.threshold_to_meet)<= 0.6:
                self.click_count += 1  # increment click count again
                if self.click_count == 2:
                    if primary_card == self.piles[pile_index][-1]:   # Check if the double-clicked card is the top card in the pile
                        self.move_card_to_foundation(primary_card)  # Sends card to the location
                        if self.game_mode_flag == False:
                            self.show_talon_cards()
                    self.click_count = 0 # reset the count
            else:
                self.click_count = 1
            self.threshold_to_meet = first_clicked



            # standard rule
            if  self.game_mode_flag and pile_index == STOCK_PILE:
                # Check if there are cards in the Stock Pile
                if len(self.piles[STOCK_PILE]) > 0:
                    # Flip the top card from the Stock Pile to the Talon Pile
                    card = self.piles[STOCK_PILE][-1]
                    card.face_up()
                    card.position = self.pile_mat_list[TALON_PILE].position
                    self.piles[STOCK_PILE].remove(card)
                    self.piles[TALON_PILE].append(card)
                    self.pull_to_top(card)


            # Vegas rule
            # If we click on the stock, 3 cards move to the talon pile
            if not self.game_mode_flag and pile_index == STOCK_PILE:


                self.get_3_talon_cards()




            elif primary_card.is_face_down():
                primary_card.face_up()



            else:
                # All other cases, grab the face-up card
                self.held_cards = [primary_card]
                # Save the position
                self.held_cards_original_position = [self.held_cards[0].position]
                # Put on top of Stock
                self.pull_to_top(self.held_cards[0])

                # If stack, grab rest of pile too
                if primary_card in self.piles[pile_index]: # primary key must be in a pile
                    card_index = self.piles[pile_index].index(primary_card)

                    for i in range(card_index + 1, len(self.piles[pile_index])):
                        card = self.piles[pile_index][i]
                        self.held_cards.append(card)
                        self.held_cards_original_position.append(card.position)
                        self.pull_to_top(card)

        # If mats are found and Stock Pile is empty
        elif len(mats) > 0 and len(self.piles[STOCK_PILE]) == 0:
            mat = mats[0]
            mat_index = self.pile_mat_list.index(mat)

            if mat_index == STOCK_PILE:
                # When Stock Pile is empty, move all cards from Talon Pile back to Stock Pile
                while self.piles[TALON_PILE]:
                    card = self.piles[TALON_PILE].pop()
                    card.face_down()
                    card.position = self.pile_mat_list[STOCK_PILE].position
                    self.piles[STOCK_PILE].append(card)

        # If cards are not found
        else:

            # You didn't click on a card
            mats = arcade.get_sprites_at_point((x, y), self.pile_mat_list)

            if len(mats) > 0:
                mat = mats[0]
                mat_index = self.pile_mat_list.index(mat)

                if mat_index == STOCK_PILE and len(self.piles[STOCK_PILE]) == 0:
                    # Flip stock pile so we can restart
                    temp_list = self.piles[STOCK_PILE].copy()
                    for card in reversed(temp_list):
                        card.face_down()
                        self.piles[TALON_PILE].remove(card)
                        self.piles[STOCK_PILE].append(card)
                        card.position = self.pile_mat_list[STOCK_PILE].position

    def get_3_talon_cards(self):
        # Flip the 3 new cards
        for i in range(3):
            # If there is no more cards, stop
            if len(self.piles[STOCK_PILE]) == 0:
                break

            # Go back to the top of the stock pile
            card = self.piles[STOCK_PILE][-1]

            # Now flip that card
            card.face_up()

            # Position of the talon with downward shift for Vegas mode
            card.position = (
                self.pile_mat_list[TALON_PILE].position[0],
                self.pile_mat_list[TALON_PILE].position[1] - i * (CARD_VERTICAL_OFFSET+10)
            )
            print(card.position, "card position")
            # Remove the card from the stock
            self.piles[STOCK_PILE].remove(card)
            # Move the card to the talon
            self.piles[TALON_PILE].append(card)
            # Put the new cards at the top of the pile
            self.pull_to_top(card)

    def move_card_to_foundation(self, primary_card):
        """Validates the rules for stacking in the foundations and moves the card to foundation if they are met"""
        if primary_card.is_face_down():
            # The card must be face up to move to the foundation
            return False

        card_suit = primary_card.get_suit()
        card_value = primary_card.get_value()

        # Iterate through the foundation piles
        for pile_index in range(FOUNDATION_PILE_1, FOUNDATION_PILE_4 + 1):
            target_pile = self.piles[pile_index] # Destination of the card

            if card_value == 1: # If it's an Ace
                if len(target_pile) == 0: # If foundation is empty
                    primary_card.position = self.pile_mat_list[pile_index].position # Matches the pos of card and foundation (move card to foundation)
                    self.move_card_to_new_pile(primary_card, pile_index)
                    return True  # Card successfully moved to the foundation pile
            else:
                if len(target_pile) > 0: # Foundation pile is not empty, then card can be stacked
                    top_card = target_pile[-1] # The card on the foundation pile to be compared to primary card for stacking
                    if card_suit == top_card.get_suit() and (int(card_value) == int(top_card.get_value()) + 1): # Cards' suit match and Values is in ascending order
                        primary_card.position = self.pile_mat_list[pile_index].position # Matches the pos of card and foundation (move card to foundation)
                        self.move_card_to_new_pile(primary_card, pile_index)
                        return True  # Card successfully moved to the foundation pile
        return False

    def remove_card_from_pile(self, card):
        # remove a card from the pile that it was in
        for pile in self.piles:
            if card in pile:
                pile.remove(card)
                break

    def get_pile_for_card(self, card):
        # This looks to see which pile the card is in
        for index, pile in enumerate(self.piles):
            if card in pile:
                return index

    def move_card_to_new_pile(self, card, pile_index):
        """Removes card from previous pile and add it to new pile target"""
        self.remove_card_from_pile(card)
        self.piles[pile_index].append(card)

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """ Called when the user presses a mouse button. """

        # if held_cards is empty list
        if len(self.held_cards) == 0:
        # if self.held_cards[0] != 0:
            return

        # Find the closest pile, in case we are in contact with more than one
        # if self.held_cards[0] != 0:
        pile, distance = arcade.get_closest_sprite(self.held_cards[0], self.pile_mat_list)

        reset_position = True


        # See if we are in contact with the closest pile
        if arcade.check_for_collision(self.held_cards[0], pile):
            card_orignal_from = self.get_pile_for_card(self.held_cards[0])
            # Which pile is going to place to?
            pile_index = self.pile_mat_list.index(pile)

            #  Is it the same pile we came from?
            if pile_index == self.get_pile_for_card(self.held_cards[0]):
                # If so, who cares. We'll just reset our position.
                pass

            # move to tableau pile
            elif TABLEAU_PILE_1 <= pile_index <= TABLEAU_PILE_7:
                # if pile is not empty
                if len(self.piles[pile_index]) > 0:
                    top_card = self.piles[pile_index][-1]
                    primary_color = self.held_cards[0].get_color()
                    top_color = top_card.get_color()
                    primary_value = int(self.held_cards[0].get_value())
                    top_value = int(top_card.get_value())

                    #if the primary card is the opposite color of the top card and the primary card is one less than the top card
                    if primary_color != top_color and primary_value == top_value - 1:
                        for i, dropped_card in enumerate(self.held_cards):
                            dropped_card.position = top_card.center_x, top_card.center_y - CARD_VERTICAL_OFFSET * (
                                    i + 1)
                        # Cards are in the right position, but we need to move them to the right list
                        for card in self.held_cards:
                            self.move_card_to_new_pile(card, pile_index)

                        # Success, don't reset position of cards
                        reset_position = False

                else:
                    # If the target pile is empty and the prime card of held cards is a King (value is 13),
                    # move it to the empty pile
                    if self.held_cards[0].get_value() == 13:
                        for i, dropped_card in enumerate(self.held_cards):
                            dropped_card.position = pile.center_x, pile.center_y - CARD_VERTICAL_OFFSET * i
                        for card in self.held_cards:
                            self.move_card_to_new_pile(card, pile_index)
                        reset_position = False



            # Move to foundation pile
            elif FOUNDATION_PILE_1 <= pile_index <= FOUNDATION_PILE_4 and len(self.held_cards) == 1:
                target_pile = self.piles[pile_index]

                if len(target_pile) == 0:
                    # If the target pile is empty, only Ace (A) can be moved to an empty pile
                    if self.held_cards[0].get_value() == 1:
                        # Check if the card's suit matches the foundation pile's suit
                        target_suit = target_pile[0].get_suit() if len(target_pile) > 0 else None
                        held_suit = self.held_cards[0].get_suit()
                        if target_suit is None or target_suit == held_suit:
                            # Move the card to the foundation pile
                            self.held_cards[0].position = pile.position
                            for card in self.held_cards:
                                self.move_card_to_new_pile(card, pile_index)
                            reset_position = False
                else:
                    # If the target pile is not empty, check if the card's value is one greater than the top card's value
                    top_card = target_pile[-1]
                    primary_value = self.held_cards[0].get_value()
                    top_value = top_card.get_value()
                    if primary_value == top_value + 1:
                        # Check if the card's suit matches the foundation pile's suit
                        target_suit = top_card.get_suit()
                        held_suit = self.held_cards[0].get_suit()
                        if target_suit == held_suit:
                            # Move the card to the foundation pile
                            self.held_cards[0].position = pile.position
                            for card in self.held_cards:
                                self.move_card_to_new_pile(card, pile_index)
                            reset_position = False


            if not reset_position and card_orignal_from == TALON_PILE and self.game_mode_flag == False:
                # Show 3 Talon cards if cards were successfully moved and the source pile was Talon
                self.show_talon_cards()

        if reset_position:
            #            # Where-ever we were dropped, it wasn't valid. Reset the each card's position
            #            # to its original spot.
            for pile_index, card in enumerate(self.held_cards):
                card.position = self.held_cards_original_position[pile_index]

        #        # We are no longer holding cards
        self.held_cards = []

    def on_mouse_motion(self, x: float, y: float, dx: int, dy: int):
        """ User moves mouse and drags the selected/held card """

        # If a card is clicked, then move it along the mouse
        # if self.held_cards != [0]:
        if self.held_cards != [0]:
            for card in self.held_cards:
                card.center_x += dx
                card.center_y += dy

    def on_key_press(self, symbol: int, modifiers: int):
        """ User presses key """
        if symbol == arcade.key.R:
            # Restart
            self.setup()
        elif symbol == arcade.key.S:
            # Switch game mode
            self.setup()
            self.game_mode_flag = not self.game_mode_flag

    def show_talon_cards(self):
        """Show the top 3 cards in Talon Pile"""

        # Get the Talon Pile
        talon_pile = self.piles[TALON_PILE]

        # Make sure there are at least 3 cards in Talon Pile
        if len(talon_pile) >= 3:
            # Iterate over the top 3 cards in Talon Pile
            for i in range(2,-1, -1):
                card = talon_pile[-1 - i]  # Get the topmost card
                # print(card.get_value(), card.get_suit())
                card.face_up()  # Make sure the card is face up
                card.position = (
                    self.pile_mat_list[TALON_PILE].center_x,
                    self.pile_mat_list[TALON_PILE].center_y + (i-2) * (CARD_VERTICAL_OFFSET+10)
                )

                # Ensure the card is in the card list and on top
                self.pull_to_top(card)



def main():
    """ Main function """
    window = Solitaire()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()