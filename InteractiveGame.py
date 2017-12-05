import os

# Import other modules from pygame_cards if needed.
from pygame_cards import game_app, controller, enums, card_holder, deck, card
from GameState import GameState
import agents
from PlayerState import PlayerState


class InteractiveGame(controller.Controller):
    """ Main class that controls game logic and handles user events.
        Following methods are mandatory for all classes that derive from Controller:
            - build_objects()
            - start_game()
            - process_mouse_events()
        Also these methods are not mandatory, but it can be helpful to define them:
            - execute_game()
            - restart_game()
            - cleanup()
        These methods are called from higher level GameApp class.
        See details about each method below.
        Other auxiliary methods can be added if needed and called from the mandatory methods.
    """

    def build_objects(self):
        """ Create permanent game objects (deck of cards, players etc.) and
        GUI elements in this method. This method is executed during creation of GameApp object.
        """

        self.custom_dict["state"] = GameState([0]*13,[0]*13,0)


        self.custom_dict["players"] = ['Player',agents.DumbestContender()]

        deck_pos = self.settings_json["deck"]["position"]
        deck_offset = self.settings_json["deck"]["offset"]
        self.custom_dict["deck"] = deck.Deck(type_=enums.DeckType.full,
                                             pos=deck_pos, offset=deck_offset)

        player_stack_pos = self.settings_json["player_stack"]["position"]
        player_stack_offset = self.settings_json["player_stack"]["offset"]
        self.custom_dict["player_stack"] = card_holder.CardsHolder(pos=player_stack_pos, offset=player_stack_offset,grab_policy=enums.GrabPolicy.can_single_grab)

        bot_stack_pos = self.settings_json["bot_stack"]["position"]
        bot_stack_offset = self.settings_json["bot_stack"]["offset"]
        self.custom_dict["bot_stack"] = card_holder.CardsHolder(pos=bot_stack_pos, offset=bot_stack_offset)

        claim_prep_pos = self.settings_json["claim_prep"]["position"]
        claim_prep_offset = self.settings_json["claim_prep"]["offset"]
        self.custom_dict["claim_prep"] = card_holder.CardsHolder(pos=claim_prep_pos, offset=claim_prep_offset)

        claim_stack_pos = self.settings_json["claim_stack"]["position"]
        claim_stack_offset = self.settings_json["claim_stack"]["offset"]
        self.custom_dict["claim_stack"] = card_holder.CardsHolder(pos=claim_stack_pos, offset=claim_stack_offset)

        # All game objects should be added to self objects list
        #  with add_object method in order to be rendered.
        self.add_rendered_object(( self.custom_dict["player_stack"],self.custom_dict["bot_stack"],self.custom_dict["claim_prep"],self.custom_dict["claim_stack"]))

        # Create Restart button
        self.gui_interface.show_button(self.settings_json["button"]["restart_button"],
                                       self.restart_game, "Restart")

        self.gui_interface.show_button(self.settings_json["button"]["plus_button"],
                                       self.player_claim, "+1")
        self.gui_interface.show_button(self.settings_json["button"]["stay_button"],
                                       self.player_claim, "+0")
        self.gui_interface.show_button(self.settings_json["button"]["minus_button"],
                                       self.player_claim, "-1")

        # self.gui_interface.show_label(self.settings_json["label"]["last_rank"],"Last Rank: 7")

    def start_game(self):
        """ Put game initialization code here.
            For example: dealing of cards, initialization of game timer etc.
            This method is triggered by GameApp.execute().
        """

        # Shuffle cards in the deck
        self.custom_dict["deck"].shuffle()

        while self.custom_dict["deck"].cards:
            card_ = self.custom_dict["deck"].pop_top_card()
            if isinstance(card_, card.Card):
                card_.flip()
                self.custom_dict["player_stack"].add_card(card_)
            card_ = self.custom_dict["deck"].pop_top_card()
            if isinstance(card_, card.Card):
                self.custom_dict["bot_stack"].add_card(card_)

        self.update_state()

    def process_mouse_event(self, pos, down, double_click):


    #     """ Put code that handles mouse events here.
    #         For example: grab card from a deck on mouse down event,
    #         drop card to a pile on mouse up event etc.
    #         This method is called every time mouse event is detected.
    #         :param pos: tuple with mouse coordinates (x, y)
    #         :param down: boolean, True for mouse down event, False for mouse up event
    #         :param double_click: boolean, True if it's a double click event
    #     """
        if down:
            if pos[1] > 300:
                last = None
                for card_ in self.custom_dict["player_stack"].cards:
                    if card_.is_clicked(pos):
                        last = card_
                if last != None and isinstance(card_, card.Card) and len(self.custom_dict["claim_prep"].cards) < 4:
                    self.move_card(last,self.custom_dict["player_stack"],self.custom_dict["claim_prep"])
                    # self.custom_dict["claim_prep"].add_card(last)
                    # self.custom_dict["player_stack"].cards.remove(last)
            else:
                for card_ in self.custom_dict["claim_prep"].cards:
                    if card_.is_clicked(pos):
                        if isinstance(card_, card.Card):
                            self.move_card(card_,self.custom_dict["claim_prep"],self.custom_dict["player_stack"])
                            # self.custom_dict["player_stack"].add_card(card_)
                            # self.custom_dict["claim_prep"].cards.remove(card_)

        #     card_ = self.custom_dict["deck"].pop_top_card()
        #     print len(self.custom_dict["deck"].cards)
        #     if isinstance(card_, card.Card):
        #         card_.flip()
        #         self.custom_dict["player_stack"].add_card(card_)

    def restart_game(self):
        """ Put code that cleans up any current game progress and starts the game from scratch.
            start_game() method can be called here to avoid code duplication. For example,
            This method can be used after game over or as a handler of "Restart" button.
        """
        for obj in self.rendered_objects:
            obj.move_all_cards(self.custom_dict["deck"])
        # self.custom_dict["player_stack"].move_all_cards()
        # self.custom_dict["bot_stack"].move_all_cards(self.custom_dict["deck"])
        # self.custom_dict["claim_prep"].move_all_cards(self.custom_dict["deck"])
        self.start_game()

    def player_claim(self):
        # TOADD: bot can call bluff now
        self.custom_dict["claim_prep"].move_all_cards(self.custom_dict["claim_stack"])

    #adds card to sink and removes from source
    def move_card(self,card,source,sink):
        sink.add_card(card)
        source.cards.remove(card)

    def execute_game(self):
        """ This method is called in an endless loop started by GameApp.execute().
        IMPORTANT: do not put any "heavy" computations in this method!
        It is executed frequently in an endless loop during the app runtime,
        so any "heavy" code will slow down the performance.
        If you don't need to check something at every moment of the game, do not define this method.
        Possible things to do in this method:
             - Check game state conditions (game over, win etc.)
             - Run bot (virtual player) actions
             - Check timers etc.
        """
        #check if bot turn, execute bot action, check if over,
        pass

    def cleanup(self):
        """ Called when user closes the app.
            Add destruction of all objects, storing of game progress to a file etc. to this method.
        """
        for obj in self.rendered_objects:
            del obj

    def update_state(self):
        state = self.custom_dict["state"]

        player_cards = state.playerCards

        #update player_cards
        for card in self.custom_dict["player_stack"].cards:
            if card.rank != 1:
                player_cards[0][card.rank-2] += 1
            else:
                player_cards[0][12] += 1
            # player_cards[0][card.rank] += 1


        #update bot_cards
        for card in self.custom_dict["bot_stack"].cards:
            if card.rank != 1:
                player_cards[1][card.rank-2] += 1
            else:
                player_cards[1][12] += 1


def player_turn():
    #initiate player_turn
    pass

def bot_turn():
    #set up bot turn
    pass


def main():
    """ Entry point of the application. """

    # JSON files contains game settings like window size, position of game and gui elements etc.
    json_path = os.path.join(os.getcwd(), 'settings.json')

    # Create an instance of GameApp and pass a path to setting json file
    # and an instance of custom Controller object. This will initialize the game,
    # build_objects() from Controller will be called at this step.
    cheat_app = game_app.GameApp(json_path=json_path, game_controller=InteractiveGame())

    # Start executing the game. This will call start_game() from Controller,
    # then will be calling execute_game() in an endless loop.
    cheat_app.execute()

if __name__ == '__main__':
    main()