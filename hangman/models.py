"""models.py - This file contains the class definitions for the Datastore
entities used by the Game. Because these classes are also regular Python
classes they can include methods (such as 'to_form' and 'new_game')."""

import random
from datetime import date
from protorpc import messages
from google.appengine.ext import ndb

class User(ndb.Model):
    """
    User Profile
    """
    name = ndb.StringProperty(required = True)
    email = ndb.StringProperty()
    wins = ndb.IntegerProperty(default = 0)
    loses = ndb.IntegerProperty(default = 0)

class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)