#!/usr/bin/env python

"""main.py - This file contains handlers that are called by taskqueue and/or
cronjobs."""
import logging

import webapp2
from google.appengine.api import mail, app_identity
from google.appengine.ext import ndb
from tictactoe_api import TicTacToeApi
from utils import get_by_urlsafe

from models import User, Game


class SendReminderEmail(webapp2.RequestHandler):
    def get(self):
        """Send a reminder email to each User with an email about games.
        Called every hour using a cron job"""
        app_id = app_identity.get_application_id()
        users = User.query(User.email != None)
        for user in users:
            # Games in progress
            games = Game.query(ndb.OR(Game.player_x == user.key,
                                      Game.player_o == user.key)).filter(Game.game_over == False)

            # Email user about game in progress
            if games.count() > 0:
                subject = 'This is a reminder!'
                body = 'Hello {}, {} games is in progress. ' \
                       'Keys are: {}'.\
                    format(user.name,
                           games.count(),
                           ', '.join(game.key.urlsafe() for game in games))
                logging.debug(body)
                # This will send test emails, the arguments to send_mail are:
                # from, to, subject, body
                mail.send_mail('noreply@{}.appspotmail.com'.format(app_id),
                           user.email,
                           subject,
                           body)

class UpdateGamesFinished(webapp2.RequestHandler):
    def post(self):
        """Update game listing announcement in memcache."""
        TicTacToeApi._cache_finished_games()
        self.response.set_status(204)


class SendMoveEmail(webapp2.RequestHandler):
    def post(self):
        """Send an email to a User that it is their turn"""
        app_id = app_identity.get_application_id()
        logging.debug('HEREERERER"')
        user = get_by_urlsafe(self.request.get('user_key'), User)
        game = get_by_urlsafe(self.request.get('game_key'), Game)
        subject = 'It\'s your turn!'
        body = '{}, It\'s your turn to play Tic Tac Toe. The game key is: {}'. \
            format(user.name, game.key.urlsafe())
        logging.debug(body)
        mail.send_mail('noreply@{}.appspotmail.com'.
                       format(app_id),
                       user.email,
                       subject,
                       body)


app = webapp2.WSGIApplication([
    ('/crons/send_reminder', SendReminderEmail),
    ('/tasks/cache_games_finished', UpdateGamesFinished),
    ('/tasks/send_move_email', SendMoveEmail)
], debug=True)
