"""models.py - This file contains the class definitions for the Datastore
entities used by the Game. Because these classes are also regular Python
classes they can include methods (such as 'to_form' and 'new_game')."""

import random
from datetime import date
from protorpc import messages
from google.appengine.ext import ndb

#list of random words to use if the user hasn't given us a word
WORDS = ["horse", "door", "baseball", "dominoes",
            "hockey", "aircraft", "password",
            "gingerbread", "shallow", "lightsaber"]

class User(ndb.Model):
    """
    User Profile
    """
    name = ndb.StringProperty(required = True)
    email = ndb.StringProperty()
    wins = ndb.IntegerProperty(default = 0)
    loses = ndb.IntegerProperty(default = 0)

class Game(ndb.Model):
    """
    Game Object
    """
    target = ndb.StringProperty(required = True)
    revealed_word = ndb.StringProperty(required = True)
    attempts_allowed = ndb.IntegerProperty(required = True)
    attempts_remaining = ndb.IntegerProperty(required = True, default = 5)
    game_over = ndb.BooleanProperty(required = True, default = False)
    user = ndb.KeyProperty(required = True, kind = 'User')
    moves = ndb.StringProperty(repeated = True)

    @classmethod
    def new_game(cls, user, target, attempts):
        """
        Creates a new game
        """
        #if the user hasn't given us a word use a random word
        if not target:
            target = WORDS[random.randint(0,9)]

        game = Game(user = user,
                    target = target,
                    revealed_word = '*' * len(target),
                    attempts_allowed = attempts,
                    attempts_remaining = attempts,
                    game_over = False,
                    moves = [])
        game.put()
        return game

    def to_form(self, message):
        """
        Returns a GameForm representation of the Game
        """
        form = GameForm()
        form.urlsafe_key = self.key.urlsafe()
        form.user_name = self.user.get().name
        form.attempts_remaining = self.attempts_remaining
        form.game_over = self.game_over
        form.message = message
        form.revealed_word = self.revealed_word
        form.moves = self.moves
        return form

class GameForm(messages.Message):
    """
    GameForm for outbound game state information
    """
    urlsafe_key = messages.StringField(1, required = True)
    attempts_remaining = messages.IntegerField(2, required = True)
    game_over = messages.BooleanField(3, required = True)
    message = messages.StringField(4, required = True)
    user_name = messages.StringField(5, required = True)
    revealed_word = messages.StringField(6, required = True)
    moves = messages.StringField(7, repeated = True)

class NewGameForm(messages.Message):
    """
    Used to create a new game
    """
    user_name = messages.StringField(1, required = True)
    target = messages.StringField(2)
    attempts = messages.IntegerField(3, default = 5)


class StringMessage(messages.Message):
    """
    StringMessage-- outbound (single) string message
    """
    message = messages.StringField(1, required=True)