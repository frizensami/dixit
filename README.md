# Dixit-Python

## Refined Spec

### Players
- 1x AI
- 2x Humans

### A round
1. Target player chooses a topic and a 'card'
2. Target player tells all other players what the 'topic' is
3. 30s countdown timer starts
4. All other players choose a card to play
5. After 30s - cards are revealed
6. All players choose what card they think is the target player's
7. Cards are revealed, points updated

### States
1. Waiting for topic
2. Waiting for all players to pick a card to play
3. Waiting for all players to choose card as target
4. Waiting for next round

### Events
- State 1: target POST topic to server
- State Transition from 1 -> 2: bcast from server = `{state: 2, topic: "topic"}`
- State 2: all players POST their picked card to `play` route
- State Transition from 2 -> 3: bcast from server = `{cards: [....]}`
- State 3: all players choose what they think is target's card w/ POST to `choose` route
- State Transition from 3 -> 4: `{target_card_was: aaa.jpg DATA}`
- State Transition for 4 -> 1: `{new_card: zzz.jpg DATA}

### Routes
Route | Purpose
--- | ---
/ | CHOOSE WHICH PLAYER YOU ARE HERE
/playerid:int | PLAYER SEES THIS PAGE
/playerid:int/play/cardnum:int | WEBSOCKETS ROUTE
/playerid:int/choose/cardnum:int | WEBSOCKETS ROUTE


## Initial Specification

1. Create a set number of topics to be asked (I.e a topic for each round played by two of us and the AI)

2. To Begin the game: AI, Player 1 and Subject X - DRAW 6 CARDS from the deck. (make it such that the AI starts first, and our testee last  to make it easier)

In AI's deck must have "Stupid card". A certain number of times the AI will place a stupid card not matching the topic.  Standardise the number of stupid cards for us also because we need to swap the decks later

3. Create an online platform where the players can select their cards to play and X can see the card played by the AI as well.

4. *set a count down timer of 30s* by which everyone must choose the best card (they think) that corresponds to the topic. ---> The correct card is revealed! (update point system)

5.  All players "draw" a new card (Because each round must still have 6 cards!!)

6. When it is subject X's turn, should have a textbox (?) that can take between 1 -10 words to describe his/her card.

Note: Program the AI to always choose the correct card. (this links back to knowing the sequence of the deck for all of us so that when its my turn the AI 'knows' which is my card and thus can always win. Removes the variable of AI getting answer wrong so that we can focus the test on its ability to put an appropriate card)
Repeat for each round
