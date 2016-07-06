#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import logging
import webapp2
from google.appengine.api import mail, app_identity
from api import Hangman
from models import User

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

class SendReminderEmail(webapp2.RequestHandler):
    def get(self):
        """
        Send a reminder e-mail to users with e-mails address who has 
        imcomplete games
        """
        app_id = app_identity.get_application_id()
        users = user.query(User.email != None)
        for user in users:
            subject = "You have an unfinished game of Hangman"
            body = "Hello {}, you have an unfinished game of hangman".format(user.name)
            mail.send_mail('noreply@{}.appspotmail.com'.format(app_id),
                           user.email,
                           subject,
                           body)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/crons/send_reminder', SendReminderEmail)
], debug=True)
