# -*- coding: utf-8 -*-
# This code is part of QKDSimkit.
#
# SPDX-License-Identifier: MIT
#
# (C) Copyright 2021 CERN.

import base64
import hashlib
import logging
import os

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def validate(shared_key: list, other_shared_key: list) -> float:
    """It compares two keys to find differences
    Args:
        shared_key (str): first key
        other_shared_key (str): second key
    Returns:
        percent of equal elements in the two keys
    """
    if len(shared_key) > 0 and len(shared_key) == len(other_shared_key):
        i = 0
        count = 0
        while i < len(shared_key):
            if shared_key[i] == other_shared_key[i]:
                count += 1
            i += 1
        return count / len(shared_key)
    else:
        logging.error("Error")
        return -1


def encrypt(token: bytes, message: str) -> str:
    """Encrypts a message using a given key

    Args:
        token (bytes): key (32 url-safe base64-encoded bytes)
        message (str): clear text message
    Returns:
         encrypted message (str)
        """
    cipher = Fernet(token)
    enc_message = cipher.encrypt(message.encode())
    return enc_message.decode()


def decrypt(token: bytes, message: str) -> str:
    """Decrypts a message using a given key

    Args:
        token (bytes): key (32 url-safe base64-encoded bytes)
        message (str): encrypted message
    Returns:
        clear text message (str)
        """
    cipher = Fernet(token)
    dec_message = cipher.decrypt(message.encode())
    return dec_message.decode()


def hash_token(token: str):
    """hash a string
    Args:
        token (str): message
    Returns: hash (str)
    """
    h = hashlib.new('sha512_256')
    h.update(token.encode())
    return h.hexdigest()


def generate_token(password):
    """Generates a com"""
    salt = b'1234567890123456'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode())).decode()
