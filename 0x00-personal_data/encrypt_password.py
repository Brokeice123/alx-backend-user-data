#!/usr/bin/env python3
"""
password encryption
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ 
    Method that hashes a password with bcrypt.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Method that checks if a provided password matches the hashed password.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)