# -*- coding: utf-8 -*-`
"""api.py - Create and configure the Game API exposing the resources.
This can also contain game logic. For more complex games it would be wise to
move game logic to another file. Ideally the API will be simple, concerned
primarily with communication to/from the API's users."""


import logging
import endpoints
from protorpc import remote, messages
from google.appengine.api import memcache
from google.appengine.api import taskqueue

from models import User, Game
from models import StringMessage, NewGameForm, GameForm, MakeMoveForm
import util

USER_REQUEST = endpoints.ResourceContainer(user_name = messages.StringField(1),
                                           email = messages.StringField(2))
NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)
MAKE_MOVE_REQUEST = endpoints.ResourceContainer(
    MakeMoveForm,
    urlsafe_game_key=messages.StringField(1),)

@endpoints.api(name = "hangman", version = "v1")
class Hangman(remote.Service):
    @endpoints.method(request_message = USER_REQUEST,
                      response_message = StringMessage,
                      path = 'user',
                      name = 'create_user',
                      http_method = 'POST')
    def create_user(self, request):
        """
        Creates a new User. Username is required
        """
        if User.query(User.name == request.user_name).get():
            raise endpoints.ConflictException(
                "Username: %s is already taken!" % request.user_name)
        user = User(name = request.user_name, email = request.email)
        user.put()
        return StringMessage(message = "User {} created".format(
                request.user_name))

    @endpoints.method(request_message = NEW_GAME_REQUEST,
                      response_message = GameForm,
                      path = 'game',
                      name = 'new_game',
                      http_method = 'POST')
    def new_game(self, request):
        """
        Creates a new hangman game. The word will be selected randomly from
        a file
        """
        user = User.query(User.name == request.user_name).get()
        if not user:
            raise endpoints.NotFoundException(
                    "Username: %s not found" % request.user_name)
        # new game can't fail (we are garenteed a username, the other 2)
        # options are optional so we don't need a try
        game = Game.new_game(user.key, request.target, request.attempts)
        return game.to_form("Good Luck")


    @endpoints.method(request_message=MAKE_MOVE_REQUEST,
                      response_message=GameForm,
                      path='game/{urlsafe_game_key}',
                      name='make_move',
                      http_method='PUT')
    def make_move(self, request):
        """
        Alows the user to make a single move in Hangman
        """
        game = util.get_by_urlsafe(request.urlsafe_game_key, Game)
        #If the user trys to make a move in a copleted game let them know 
        #the game is over
        if game.game_over:
            return game.to_form("The Game is over")

        #if the user has guessed the word complete the game
        if request.guess == game.target:
            return game.to_form(self._winner(game))

        #The User is only allowed to guess one charater at a time
        if len(request.guess) != 1:
            raise endpoints.BadRequestException(
                "Guess one letter at a time")

        #Check to see if the users has Found a letter or not
        hit_or_miss = "Miss"
        for i in range(len(game.target)):
            if game.target[i].lower() == request.guess.lower():
                game.revealed_word = game.revealed_word[:i] + \
                    game.target[i] + game.revealed_word[i+1:]
                hit_or_miss = "Hit"
        if hit_or_miss == "Miss":
            game.attempts_remaining -= 1

        move_history = "Guess: '%s', Result: '%s'" % (
            request.guess, game.revealed_word)
        game.moves.append(move_history)

        #Now check to see if the user has 
        if game.revealed_word == game.target:
            return game.to_form(self._winner(game))

        #check to see if the player has lost
        if game.attempts_remaining < 1:
            lose_text = "Game Over"
            game.moves.append(lose_text)
            game.end_game(False)
            return game.to_form(lose_text)
        #If the user hasn't lost then move on to the next move
        else:
            game.put()
            return game.to_form(hit_or_miss)


    def _winner(self, game):
        """
        Called in the different cases we have a winner
        """
        winner_text = "You Win!"
        game.moves.append(winner_text)
        game.end_game(True)
        return winner_text


api = endpoints.api_server([Hangman])