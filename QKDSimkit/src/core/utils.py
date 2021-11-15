import logging
import hashlib
from cryptography.fernet import Fernet
import os
#from Crypto.Cipher import AES


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


'''def decrypt_file(key: bytearray, filename: str):
    """It creates a new decrypted file using AES, the decrypted file will be in the same directory and it will have the
    original name except for the final '.enc'

    Args:
        key (bytearray): key to decrypt the file encrypted with AES, it has to be 128, 192, or 256 bits long
        filename (str): absolute name of the file to dencrypt
    """
    try:
        with open(filename, 'rb') as file_in:
            nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        with open(filename[:-4], 'wb') as file_out:
            file_out.write(data)
            file_out.close()
    except Exception as e:
        logging.error("failed to decrypt:\n" + str(e))
        try:
            os.remove(filename)
        except FileNotFoundError:
            logging.warning('File not found')
            pass
        raise Exception

def encrypt_file(key: bytearray, filename: str):
    """It creates a new encrypted file using AES, the encrypted file will be in the same directory and it will have the
    original name followed by'.enc' at the end

    Args:
        key (bytearray): key to decrypt the file encrypted with AES, it has to be 128, 192, or 256 bits long
        filename (str): absolute name of the file to encrypt
    """
    try:
        with open(filename, 'rb') as infile:
            chunk = infile.read()
            cipher = AES.new(key, AES.MODE_EAX)
            ciphertext, tag = cipher.encrypt_and_digest(chunk)
        with open(filename + '.enc', 'wb') as file_out:
            [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
            file_out.close()
    except Exception as e:
        logging.error('IO error during encryption: \n' + str(e))
        try:
            os.remove(filename + '.enc')
        except FileNotFoundError:
            logging.warning('File not found')
            pass
        raise Exception
'''