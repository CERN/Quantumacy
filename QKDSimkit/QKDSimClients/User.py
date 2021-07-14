import time
import os
import json
from Crypto.Cipher import AES
from QKD_Bob import import_key
from ftplib import FTP


def startClient(username, password, path):
    try:
        print('Connecting to Server: ')
        ftp = FTP('127.0.0.1')
    except ConnectionError as e:
        print('FTP error:\n' + str(e))

    ftp.set_debuglevel(1)

    try:
        ftp.login(username, password)
    except Exception as e:
        print('Wrong username or password:\n' + str(e))

    print("logged")

    try:
        bits = import_key()
        key = [int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8)][:16]
        key = bytearray(key)
        print("Key:" + str(key))
    except Exception as e:
        print('Failed to retrieve symmetric key:\n' + str(e))

    try:
        for file in os.listdir(path):
            try:
                print("Encrypting " + file)
                encrypt_file(key, path + file, path + 'tmp')
            except Exception as e:
                print('encryption failed:\n' + str(e))
            localfile = open(path + 'tmp', "rb")
            try:
                print("[!] File Transfer in Progress....")
                result = ftp.storbinary("STOR " + file, localfile)
            except Exception as e:
                print('Transfer failed:\n' + str(e))
            else:
                print(str(result))
    except Exception as e:
        print("Failed to retrieve file to send:\n" + str(e))

    try:
        os.remove(path + 'tmp')
        ftp.quit()
    except Exception as e:
        print('Failed to terminate communication:\n' + str(e))


def encrypt_file(key, in_filename, out_filename):
    try:
        with open(in_filename, 'rb') as infile:
            chunk = infile.read()
            try:
                cipher = AES.new(key, AES.MODE_EAX)
                ciphertext, tag = cipher.encrypt_and_digest(chunk)
            except Exception as e:
                print("key or value error: \n" + str(e))
            with open(out_filename, 'wb') as file_out:
                [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
                file_out.close()
    except Exception as e:
        print('IO error during encryption: \n' + str(e))


startClient('user0', '12345', '../data/source/')
