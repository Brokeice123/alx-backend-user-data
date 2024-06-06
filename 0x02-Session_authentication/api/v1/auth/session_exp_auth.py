#!/usr/bin/env python3
""" SessionExpAuth module
"""
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from os import getenv

class SessionExpAuth(SessionAuth):
    """ SessionExpAuth class that inherits from SessionAuth """

    def __init__(self):
        """ Initialize the instance with session duration """
        super().__init__()
        try:
            self.session_duration = int(getenv('SESSION_DURATION'))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """ Create a session with an expiration """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Retrieve user_id from session_id with expiration check """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        created_at = session_dict.get('created_at')
        if created_at is None:
            return None

        if created_at + timedelta(seconds=self.session_duration) < datetime.now():
            return None

        return session_dict.get('user_id')
