#!/usr/bin/env python3
"""
Auth file
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash a password with bcrypt and return the hashed password as bytes"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password