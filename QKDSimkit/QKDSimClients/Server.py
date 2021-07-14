import time
import os
import json
import logging
from QKD_Alice import import_key
from Crypto.Cipher import AES
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer


logging.basicConfig(level=logging.DEBUG)


class MyHandler(FTPHandler):  # FTP server handler
    def on_file_received(self, filename):  # Once the file is received by the server, trigger this event
        decrypt_file(self.key, filename)

    def on_login(self, user):
        try:
            bits = import_key()
            self.key = [int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8)][:16]
            self.key = bytearray(self.key)
        except Exception as e:
            print('Failed to retrieve key:\n' + str(e))

    def on_login_failed(self, username, password):
        print(username + " failed to login")


def startServer():
    try:
        authorizer = DummyAuthorizer()
        with open('../data/users.json', 'r') as users:
            authorizer.user_table = json.load(users)
    except Exception as e:
        print("Failed to load user table (may be a permission issue or a duplicate user): \n" + str(e))

    try:
        handler = MyHandler  # select the created custom FTP handler
        handler.authorizer = authorizer  # assign the authorizer to the handler
        handler.banner = "Server Ready.."  # server banner is returned when the client calls a getWelcomeMessage() call
        address = ('', 21)
        server = FTPServer(address, handler)
        server.max_cons = 10
        server.serve_forever()  # start the server
    except Exception as e:
        print("Server failed to start:\n" + str(e))

def decrypt_file(key, filename):
    try:
        with open(filename, 'rb') as file_in:
            nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        with open(filename, 'wb') as file_out:
            file_out.write(data)
            file_out.close()
    except Exception as e:
        print("failed to decrypt:\n" + str(e))


def add_user(user, password, auth):
    with open('../data/users.json', 'r') as users:
        auth.user_table = json.load(users)
        users.close()
    os.mkdir('../data/' + user)
    auth.add_user(user, password, '../data/' + user, perm='rw')
    with open('../data/users.json', 'w') as users:
        json.dump(auth.user_table, users)
        users.close()


startServer()
