class Player:

    def reset(self):
        self.playerid = 0
        self.deck = []
        self.chosen_card = None
        self.other_cards = None
        self.guess = None

    def __init__(self, playerid=0, deck=[]):
        self.reset()
        self.playerid = playerid
        self.deck = deck

    def __repr__(self):
        return "id: %s, deck: %s, chosen_card: %s, other_cards: %s, guess: %s" % \
            (str(self.playerid), str(self.deck), str(self.chosen_card), str(self.other_cards), str(self.guess))


class STATE:
    WAIT_TOPIC = 0
    WAIT_CARD = 3
    ALL_PICK = 1
    ALL_CHOOSE_TARGET = 2


class Game:




    def reset(self):
        self.started = False
        self.state = STATE.WAIT_TOPIC
        self.players = []
        self.current_target_player = None
        self.topic = None
        self.send_topic_callback = None
        self.send_pick_target_callback = None
        self.send_after_guess_callback = None

        # This defines the deck distribution for each player
        # i.e. first list = player 0 cards, second = player 1 etc
        self.decks = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                 [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
                 [21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
                 ]

    def __init__(self, num_players=1, starting_player_num=0, send_topic_callback=None,
                 send_pick_target_callback=None, send_after_guess_callback=None):
        self.reset()
        for i in xrange(num_players):
            print "Adding player: " + str(i)
            new_player = Player(playerid=i, deck=self.decks[i])
            self.players.append(new_player)

            # Sets the starting player
            self.current_target_player = starting_player_num

        self.state = STATE.WAIT_TOPIC
        self.send_topic_callback = send_topic_callback
        self.send_pick_target_callback = send_pick_target_callback
        self.send_after_guess_callback = send_after_guess_callback

    def set_topic(self, topic):
        self.topic = topic

    def begin(self):
        if not self.started:
            self.started = True
            return True
        else:
            return False

    def start_next_round():
        print "Starting next round!"

    def notify_deck_card_clicked(self, player_id, card_id):
        if self.started and (player_id == self.current_target_player) and self.state == STATE.WAIT_CARD:
            print "New valid deck card %s selected as target by current player %s" % (card_id, player_id)
            self.players[player_id].chosen_card = self.players[player_id].deck[card_id]
            self.players[player_id].guess = self.players[player_id].deck[card_id]
            self.send_topic_callback(self.topic)
            self.state = STATE.ALL_PICK

        elif self.started and self.state == STATE.ALL_PICK:
            print "New valid deck card %s picked as target by current player %s" % (card_id, player_id)
            self.players[player_id].chosen_card = self.players[player_id].deck[card_id]
            if self.all_players_have_chosen_a_card():
                other_cards_for_players = self.resolve_chosen_cards_for_players()
                self.send_pick_target_callback(other_cards_for_players)
                self.state = STATE.ALL_CHOOSE_TARGET

    def notify_other_card_clicked(self, player_id, card_id):
        if self.started and self.state == STATE.ALL_CHOOSE_TARGET:
            self.players[player_id].guess = self.players[player_id].other_cards[card_id]
            if self.all_players_have_guessed():
                # Send back if they are correct?
                self.send_after_guess_callback(self.players[self.current_target_player].chosen_card)
                self.start_next_round()



    def notify_new_topic(self, player_id, topic_text):
        if self.started and (player_id == self.current_target_player) and self.state == STATE.WAIT_TOPIC:
            print "New valid topic: %s from %s" % (topic_text, player_id)
            self.topic = topic_text
            self.state = STATE.WAIT_CARD
            return True
        else:
            return False

    def all_players_have_chosen_a_card(self):
        # If we filter the players list for a player that hasn't chosen a card
        # and get a non zero length - we have an undecided player
        return len(filter(lambda player: player.chosen_card is None, self.players)) == 0

    def all_players_have_guessed(self):
        # If we filter the players list for a player that hasn't chosen a card
        # and get a non zero length - we have an undecided player
        return len(filter(lambda player: player.guess is None, self.players)) == 0

    def resolve_chosen_cards_for_players(self):
        # Assumes all players have chosen cards
        # Returns a list of card numbers for each player to display on the screen
        # E.g. {0: [2, 3], 1: [5, 6], 2: [7, 8]} means player 0 will be displayed 2 and 3, etc
        out_dict = {}
        print "Players: " + str(self.players)
        for index in range(0, len(self.players)):
            # For each player
            not_me_players = filter(lambda player: player.playerid != index, self.players)
            out_dict[index] = map(lambda player: player.chosen_card, not_me_players)
            self.players[index].other_cards = out_dict[index]


        return out_dict




