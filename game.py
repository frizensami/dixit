class Player:

    def reset(self):
        self.playerid = 0
        self.deck = []
        self.chosen_card = None
        self.other_cards = None
        self.guess = None
        self.points = 0

    def next_round(self):
        # Assume points have already been tabulated
        print "player %s going to next round!" % self.playerid
        # Remove the card we chose from our deck
        self.deck.remove(self.chosen_card)

        # Clear everything we chose
        self.chosen_card = None
        self.other_cards = None
        self.guess = None

    def __init__(self, playerid=0, deck=[]):
        self.reset()
        self.playerid = playerid
        self.deck = deck

    def __repr__(self):
        return "id: %s, deck: %s, chosen_card: %s, other_cards: %s, guess: %s, points: %s" % \
            (str(self.playerid), str(self.deck), str(self.chosen_card),
             str(self.other_cards), str(self.guess), str(self.points))


class STATE:
    WAIT_TOPIC = 0
    WAIT_CARD = 3
    ALL_PICK = 1
    ALL_CHOOSE_TARGET = 2
    WAITING_FOR_NEXT_ROUND = 4


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
        self.num_players = 0

        # This defines the deck distribution for each player
        # i.e. first list = player 0 cards, second = player 1 etc
        self.decks = [[48, 1, 30, 40, 16, 19, 32, 11, 7, 37, 46],
                      [44, 22, 26, 36, 9, 47, 6, 31, 50, 3, 29],
                      [45, 20, 25, 33, 17, 28, 49, 42, 5, 35, 39]
                      ]

    def __init__(self, num_players=1, starting_player_num=0, send_topic_callback=None,
                 send_pick_target_callback=None, send_after_guess_callback=None):
        self.reset()
        self.num_players = num_players
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

    def start_next_round(self):
        if self.state == STATE.WAITING_FOR_NEXT_ROUND:
            print "Successfully starting next round!"

            print "=====PLAYER STATE BEFORE NEXT ROUND====="
            for player in self.players:
                print str(player)
            '''
            Todo list to start new round:
            1) Tabulate points for each player
            2) Ask player to set themselves up for next round
            3) Choose next target player
            '''
            # WARNING - this algo will give 1 point to the current target
            # player no matter what
            correct_card = self.players[self.current_target_player].chosen_card
            for player in self.players:
                if player.guess == correct_card:
                    print "increasing points for player %s" % player.playerid
                    player.points += 1

                player.next_round()

            self.current_target_player = (
                self.current_target_player + 1) % self.num_players
            self.state = STATE.WAIT_TOPIC
            print "New current target player: %s" % str(self.current_target_player)

            print "=====PLAYER STATE AFTER NEXT ROUND HAS STARTED====="
            for player in self.players:
                print str(player)

            return True

        else:
            print "Cannot start next round!"
            return False

    def notify_deck_card_clicked(self, player_id, card_id):
        if self.started and (player_id == self.current_target_player) and self.state == STATE.WAIT_CARD:
            print "New valid deck card %s selected as target by current player %s" % (card_id, player_id)
            self.players[player_id].chosen_card = self.players[
                player_id].deck[card_id]
            self.players[player_id].guess = self.players[
                player_id].deck[card_id]
            self.send_topic_callback(self.topic)
            self.state = STATE.ALL_PICK

        elif self.started and self.state == STATE.ALL_PICK:
            print "New valid deck card %s picked as target by current player %s" % (card_id, player_id)
            self.players[player_id].chosen_card = self.players[
                player_id].deck[card_id]
            if self.all_players_have_chosen_a_card():
                other_cards_for_players = self.resolve_chosen_cards_for_players()
                self.send_pick_target_callback(other_cards_for_players)
                self.state = STATE.ALL_CHOOSE_TARGET

    def notify_other_card_clicked(self, player_id, card_id):
        if self.started and self.state == STATE.ALL_CHOOSE_TARGET:
            self.players[player_id].guess = self.players[
                player_id].other_cards[card_id]
            if self.all_players_have_guessed():
                # Send back if they are correct?
                self.send_after_guess_callback(
                    self.resolve_guessed_cards_for_players())
                self.state = STATE.WAITING_FOR_NEXT_ROUND

    def notify_new_topic(self, player_id, topic_text):
        if self.started and (player_id == self.current_target_player) and self.state == STATE.WAIT_TOPIC:
            print "New valid topic: %s from %s" % (topic_text, player_id)
            self.topic = topic_text
            self.state = STATE.WAIT_CARD
            return True
        else:
            print str(self.started)
            print str(player_id)
            print str(self.current_target_player)
            print str(self.state)
            print self.started == True
            print player_id == self.current_target_player
            print self.state == STATE.WAIT_TOPIC
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
        # E.g. {0: [2, 3], 1: [5, 6], 2: [7, 8]} means player 0 will be
        # displayed 2 and 3, etc
        out_dict = {}
        print "Players: " + str(self.players)
        for index in range(0, len(self.players)):
            # For each player
            not_me_players = filter(
                lambda player: player.playerid != index, self.players)
            out_dict[index] = map(
                lambda player: player.chosen_card, not_me_players)
            self.players[index].other_cards = out_dict[index]

        return out_dict

    def resolve_guessed_cards_for_players(self):
        # Assumes all players have chosen cards
        # Returns to each player which card is correct etc
        # E.g. {0: [0 1] means that for their other cards: true/false
        out_dict = {}
        print "Players: " + str(self.players)
        for index in range(0, len(self.players)):
            # Checks for each of the player's "other_cards" - which is the real
            # card
            out_dict[index] = map(lambda card: card == self.players[self.current_target_player].chosen_card,
                                  self.players[index].other_cards)

        return out_dict
