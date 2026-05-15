# Competitive-AI-for-GoFish

This project will focus on implementing a competitive Go Fish-play agent. The AI opponent will estimate the likelihood that the player holds cards of specific ranks based on card requests, successful or unsuccessful exchanges, and cards set aside for completed sets. The AI opponent will constantly update its possibilities based on the player's actions to improve its chances of winning.

goFish.py: Entry point

goFish folder contains the player and bot logic, gameplay loop, and cards.
	goFish/game.py: This file includes the main gameplay logic: gameover, draw card, check for books, sorting hands, or player rotations.
	goFish/bot.py: This file includes the bot logic: Changing probabilty when player or bot asks for a card and the resulting action. The bot has it's own completed book cause they know for sure that the rank they booked would now have a probability of zero.
	goFish/player.py: This file includes basic player functions like checking if they have the rank or removing that cards of that rank from their hand.
	goFish/card.py: This file includes the class that creates the cards.