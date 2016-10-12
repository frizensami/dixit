class Player:
    playerid = 0
    deck = []
    chosen_card = None

    def __init__(self, playerid=0, deck=[]):
        self.playerid = playerid
        self.deck = deck


class STATE:
    WAIT_TOPIC = 0
    WAIT_CARD = 3
    ALL_PICK = 1
    ALL_CHOOSE_TARGET = 2


class Game:

    started = False
    state = STATE.WAIT_TOPIC
    players = []
    current_target_player = None
    topic = None

    # This defines the deck distribution for each player
    # i.e. first list = player 0 cards, second = player 1 etc
    decks = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
             [11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
             [21, 22, 23, 24, 25, 26, 27, 28, 29, 30],
             ]

    def reset(self):
        self.started = False
        self.state = STATE.WAIT_TOPIC
        self.players = []
        self.current_target_player = None
        self.topic = None
        self.send_topic_callback = None
        self.send_pick_target_callback = None

    def __init__(self, num_players=1, starting_player_num=0, send_topic_callback=None,
                 send_pick_target_callback=None):
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

    def set_topic(self, topic):
        self.topic = topic

    def begin(self):
        if not self.started:
            self.started = True
            return True
        else:
            return False

    def notify_deck_card_clicked(self, player_id, card_id):
        if self.started and (player_id == self.current_target_player) and self.state == STATE.WAIT_CARD:
            print "New valid deck card %s selected as target by current player %s" % (card_id, player_id)
            self.players[player_id].chosen_card = card_id
            self.send_topic_callback(self.topic)
            self.state = STATE.ALL_PICK
        elif self.started and self.state == STATE.ALL_PICK:
            print "New valid deck card %s picked as target by current player %s" % (card_id, player_id)
            self.players[player_id].chosen_card = card_id
            if self.all_players_have_chosen_a_card():
                self.send_pick_target_callback()

    def notify_other_card_clicked(self, player_id, card_id):
        pass
        '''
        if self.started and (player_id == self.current_target_player):
            print "New valid other card %s selected as target by current player %s" % (card_id, player_id)
            return True
        else:
            return False
            '''

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




