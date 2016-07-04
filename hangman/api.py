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
from models import StringMessage, NewGameForm, GameForm

USER_REQUEST = endpoints.ResourceContainer(user_name = messages.StringField(1),
                                           email = messages.StringField(2))
NEW_GAME_REQUEST = endpoints.ResourceContainer(NewGameForm)

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
        try:
            game = Game.new_game(user.key, request.target, request.attempts)
        except ValueError:
            raise endpoints.BadRequestException("Target word cannot be null")
        return game.to_form("Good Luck")


api = endpoints.api_server([Hangman])