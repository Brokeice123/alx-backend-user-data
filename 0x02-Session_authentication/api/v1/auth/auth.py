#!/usr/bin/env python3
"""
Module to handle API Authentication
"""

from os import getenv
from typing import List, TypeVar
from flask import request


class Auth():
    """
    Class that handles authentication process
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Require auth
        """
        if path is None or not excluded_paths:
            return True
        for ex_path in excluded_paths:
            if ex_path.endswith('*') and path.startswith(ex_path[:-1]):
                return False
            elif ex_path in {path, path + '/'}:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Authorization header
        """
        if request is None or 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user
        """
        return None

    def session_cookie(self, request=None):
        """ Session cookie
        """
        if request is None:
            return None
        session_name = getenv('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)
