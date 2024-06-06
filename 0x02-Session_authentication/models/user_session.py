#!/usr/bin/env python3
""" UserSession module
"""

from models.base import Base


class UserSession(Base):
    """ UserSession class for storing session data """
    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize a UserSession instance """
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
        super().__init__(*args, **kwargs)
