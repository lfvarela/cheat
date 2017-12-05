import os

# Import other modules from pygame_cards if needed.
from pygame_cards import game_app, controller, enums, card_holder, deck, card
from GameState import GameState
import agents
from PlayerState import PlayerState
import util
import copy



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
        self.custom_dict['player_choose_empty'] = False #special choose 
        self.custom_dict['midturn'] = False

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

    def addimate_card(self, stack, card_):
        """ Appends a card to the list of self.cards
        :param card_:  object of the Card class to be appended to the list
        :param on_top: bolean, True if the card should be put on top, False in the bottom
        """
        if isinstance(card_, card.Card):
            card_.unclick()
            pos_ = stack.pos
            if len(stack.cards) is not 0:
                length = len(stack.cards)
                pos_ = (stack.pos[0] + length * stack.offset[0],
                        stack.pos[1] + length * stack.offset[1])
            self.add_move([card_],pos_,16)
            stack.cards.append(card_)

    def process_mouse_event(self, pos, down, double_click):


    #     """ Put code that handles mouse events here.
    #         For example: grab card from a deck on mouse down event,
    #         drop card to a pile on mouse up event etc.
    #         This method is called every time mouse event is detected.
    #         :param pos: tuple with mouse coordinates (x, y)
    #         :param down: boolean, True for mouse down event, False for mouse up event
    #         :param double_click: boolean, True if it's a double click event
    #     """
         if self.custom_dict['state'].currentPlayer == 0 and self.custom_dict['state'].lastClaim != None:   
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

    def player_choose(self,index):
        self.custom_dict['state'].lastClaim = (index,None)
        if self.clean_restart() == False:
            self.clean_restart()
        if self.claim_prep_empty():
            self.custom_dict['player_choose_empty'] = True
            return
        self.custom_dict['player_choose_empty'] = False
        self.gui_interface.show_button(self.settings_json["button"]["go_button"],
                                       lambda: self.player_claim (0), "Go")


    def player_claim(self,offset):
        # TOADD: bot can call bluff now
        #update last rank
        claim_prep = self.custom_dict["claim_prep"]
        claim_stack = self.custom_dict["claim_stack"]
        state = self.custom_dict['state']
        # state.lastRank += offset
        #update last claim played
        state.lastClaim = (state.lastClaim[0]+offset,len(claim_prep.cards))

        #update cards played
        state.lastCardsPlayed = self.convert_cardholder(claim_prep) #will this persist????

        state.playerPutDownCards[0] = map(sum, zip(state.playerPutDownCards[0],state.lastCardsPlayed))

        state.playerClaims[0][state.lastClaim[0]] += state.lastClaim[1]

        self.clean_restart()


        claim_prep.move_all_cards(claim_stack)

        self.update_state()

        # print state.lastRank, state.lastClaim,state.lastCardsPlayed,state.playerPutDownCards,state.playerClaims[0],state.deck

        self.custom_dict['midturn'] = False
        self.custom_dict['state'].currentPlayer = 1

        #no longer midturn


    #adds card to sink and removes from source
    def move_card(self,card,source,sink):

        # write own add_card with animation
        self.addimate_card(sink,card)
        source.cards.remove(card)

        #need to fix lack of updated decks

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
        if self.custom_dict['player_choose_empty']:
            self.player_choose(self.custom_dict["state"].lastClaim[0])
        if self.custom_dict['midturn'] == False:
            if self.custom_dict["state"].lastClaim == None and self.custom_dict["state"].currentPlayer == 0:
                self.choose_number()
            else:
                if self.custom_dict["state"].currentPlayer == 0:
                    self.player_turn()
                else:
                    self.bot_turn()

    def cleanup(self):
        """ Called when user closes the app.
            Add destruction of all objects, storing of game progress to a file etc. to this method.
        """
        for obj in self.rendered_objects:
            del obj

    def update_state(self):
        state = self.custom_dict["state"]

        player_cards = state.playerCards

        player_cards[0] = self.convert_cardholder(self.custom_dict["player_stack"])
        #update player_cards

        #update bot_cards
        player_cards[1] = self.convert_cardholder(self.custom_dict["bot_stack"])

        state.deck = self.convert_cardholder(self.custom_dict["claim_stack"])

        print player_cards[0]

    # returns 13 array of card counts
    def convert_cardholder(self,cardholder):
        arr = [0]*13
        for card in cardholder.cards:
            arr[self.rank_to_index(card.rank)] += 1
        return arr

    def rank_to_index(self,rank):
        if rank != 1:
            return rank-2
        else:
            return 12


    def claim_prep_empty(self):
        return len(self.custom_dict['claim_prep'].cards) <= 0

    def player_turn(self):

        if self.claim_prep_empty():
            return

        self.custom_dict['midturn'] = True
        self.gui_interface.show_button(self.settings_json["button"]["plus_button"],
                                       lambda: self.player_claim(1), "+1")
        self.gui_interface.show_button(self.settings_json["button"]["stay_button"],
                                       lambda: self.player_claim(0), "+0")
        self.gui_interface.show_button(self.settings_json["button"]["minus_button"],
                                       lambda: self.player_claim(-1), "-1")

        #at the end clean up self.gui_interface.clean()
        pass

    def bot_turn(self):
        self.custom_dict['midturn'] = True

        state = self.custom_dict['state']
        #get action
        bot_state = state.getCurrentPlayerState()

        bot = self.custom_dict['players'][1]

        claim, action = bot.getAction(bot_state)

        print claim

        print action

        if claim == 'Bluff':
            claim, action = bot.getAction(bot_state)

        self.convert_action(action,self.custom_dict['bot_stack'])

        #set up bot turn, get action, add to bott claim
        self.gui_interface.show_button(self.settings_json["button"]["call_bluff"],
                                       lambda: self.handle_bluff(claim,action,True,0), "Call Bluff")
        self.gui_interface.show_button(self.settings_json["button"]["continue"],
                                       lambda: self.handle_bluff(claim,action,False,0), "Continue")



        #at the end clean up self.gui_interface.clean()

        pass

    def handle_bluff(self,claim,action,bluff_call,accuser):
        state = self.custom_dict['state']
        claim_stack = self.custom_dict['claim_stack']
        claim_prep = self.custom_dict['claim_prep']
        accuser_stack = None
        accusee_stack = None

        if accuser == 0:
            accuser_stack = self.custom_dict['player_stack']
            accusee_stack = self.custom_dict['bot_stack']
        else:
            accusee_stack = self.custom_dict['player_stack']
            accuser_stack = self.custom_dict['bot_stack']

        claim_prep.move_all_cards(claim_stack)

        if bluff_call:

            #if succesful bluff call for player
            if self.bluff(claim,action):

                claim_stack.move_all_cards(accusee_stack)

            #if unsuccesful bluff call
            else:
                claim_stack.move_all_cards(accuser_stack)

            state.lastClaim = None
            state.lastCardsPlayed = None

            state.playerPutDownCards = util.initEmptyDecks()
            state.playerClaims = util.initEmptyDecks()
        else:

            #update last claim played
            state.lastClaim = claim

            state.playerPutDownCards[1] = map(sum, zip(state.playerPutDownCards[1],action))

            state.playerClaims[1][state.lastClaim[0]] += state.lastClaim[1]

        #update playercards, deck
        self.update_state()

        self.clean_restart()

        self.custom_dict['midturn'] = False
        #switch to other player
        self.custom_dict['state'].currentPlayer = 0


        #converts a bot action array into claim prep
    def convert_action(self,action,stack):
        action_copy = copy.deepcopy(action)

        for card in stack.cards:
            index = self.rank_to_index(card.rank)
            if action_copy[index] > 0:
                action_copy[index] -= 1
                #self.add_move([card],self.settings_json["claim_prep"]["position"],8)
                self.move_card(card,stack,self.custom_dict['claim_prep'])


    def bluff(self,claim,action):
        return (action[claim[0]]!=claim[1])

    def choose_number(self):
        self.custom_dict['midturn'] = True
        self.gui_interface.show_button(self.settings_json["button"]["2_button"],
                                       lambda: self.player_choose(0), "2")
        self.gui_interface.show_button(self.settings_json["button"]["3_button"],
                                       lambda: self.player_choose(1), "3")
        self.gui_interface.show_button(self.settings_json["button"]["4_button"],
                                       lambda: self.player_choose(2), "4")
        self.gui_interface.show_button(self.settings_json["button"]["5_button"],
                                       lambda: self.player_choose(3), "5")
        self.gui_interface.show_button(self.settings_json["button"]["6_button"],
                                       lambda: self.player_choose(4), "6")
        self.gui_interface.show_button(self.settings_json["button"]["7_button"],
                                       lambda: self.player_choose(5), "7")
        self.gui_interface.show_button(self.settings_json["button"]["8_button"],
                                       lambda: self.player_choose(6), "8")
        self.gui_interface.show_button(self.settings_json["button"]["9_button"],
                                       lambda: self.player_choose(7), "9")
        self.gui_interface.show_button(self.settings_json["button"]["10_button"],
                                       lambda: self.player_choose(8), "10")
        self.gui_interface.show_button(self.settings_json["button"]["J_button"],
                                       lambda: self.player_choose(9), "J")
        self.gui_interface.show_button(self.settings_json["button"]["Q_button"],
                                       lambda: self.player_choose(10), "Q")
        self.gui_interface.show_button(self.settings_json["button"]["K_button"],
                                       lambda: self.player_choose(11), "K")
        self.gui_interface.show_button(self.settings_json["button"]["A_button"],
                                       lambda: self.player_choose(12), "A")
        #at the end clean up self.gui_interface.clean()

    def clean_restart(self):
        self.gui_interface.clean()
        self.gui_interface.show_button(self.settings_json["button"]["restart_button"],
                                       self.restart_game, "Restart")


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