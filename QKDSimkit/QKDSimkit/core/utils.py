# -*- coding: utf-8 -*-
# This code is part of QKDSimkit.
#
# SPDX-License-Identifier: MIT
#
# (C) Copyright 2021 CERN.

import hashlib
import logging

from cryptography.fernet import Fernet


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


def encrypt(token, message):
    cipher = Fernet(token)
    enc_message = cipher.encrypt(message.encode())
    return enc_message.decode()


def decrypt(token, message):
    cipher = Fernet(token)
    dec_message = cipher.decrypt(message.encode())
    return dec_message.decode()


def hash_token(token: str):
    h = hashlib.new('sha512_256')
    h.update(token.encode())
    return h.hexdigest()
