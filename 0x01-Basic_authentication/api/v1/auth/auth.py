#!/usr/bin/env python3
"""
Module to handle API Authentication
"""

from typing import List, TypeVar
from flask import request


class Auth():
    """
    Class that handles authentication process
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Require auth
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Current user
        """
        return None