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

from models import User
from models import StringMessage

USER_REQUEST = endpoints.ResourceContainer(user_name=messages.StringField(1),
                                           email=messages.StringField(2))

@endpoints.api(name = "hangman", version = "v1")
class Hangman(remote.Service):
    @endpoints.method(request_message=USER_REQUEST,
                      response_message=StringMessage,
                      path='user',
                      name='create_user',
                      http_method='POST')
    def create_user(self, request):
        """
        Creates a new User. Username is required
        """
        if User.query(User.name == request.user_name).get():
            raise endpoints.ConflictException(
                "Username: %s is already taken!" % User.name)
        user = User(name = request.user_name, email = request.email)
        user.put()
        return StringMessage(message = "User {} created".format(
                request.user_name))

api = endpoints.api_server([Hangman])