import sys
import os
import json
import logging
from QKD_Alice import import_key
from utils import decrypt_file, encrypt_file
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer


logging.basicConfig(level=logging.DEBUG)


class MyHandler(FTPHandler):
    def on_file_received(self, filename):
        try:
            print('Decrypting: ' + filename)
            decrypt_file(self.key, filename)
            os.remove(filename)
        except Exception as e:
            print('Failed to handle received file\n' + str(e))

    def on_incomplete_file_received(self, file):
        os.remove(file)

    def on_login(self, user):
        try:
            bits = import_key()
            self.key = [int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8)]
            self.key = bytearray(self.key)[:32]
        except Exception as e:
            print('Failed to retrieve symmetrical key:\n' + str(e))

    def on_login_failed(self, username, password):
        print(username + " failed to login")

    def ftp_RETR(self, file):
        try:
            print('Encrypting ' + file)
            encrypt_file(self.key, file)
            print(os.listdir())
            super().ftp_RETR(file + '.enc')
            os.remove(file + '.enc')
        except Exception as e:
            print("Failed to answer RETR\n" + str(e))

class Server(object):
    def startServer(self):
        try:
            authorizer = DummyAuthorizer()
            with open('../data/users.json', 'r') as users:
                authorizer.user_table = json.load(users)
        except Exception as e:
            print("Failed to load user table (may be a permission issue or a duplicate user): \n" + str(e))
            sys.exit()

        try:
            s = json.load(open('../config.json', ))['Server']
            handler = MyHandler  # select the created custom FTP handler
            handler.authorizer = authorizer  # assign the authorizer to the handler
            handler.banner = "Server Ready.."  # server banner is returned when the client calls a getWelcomeMessage() call
            address = ('', s['port'])
            server = FTPServer(address, handler)
            server.max_cons = 10
            server.serve_forever()  # start the server
        except Exception as e:
            print("Server failed to start:\n" + str(e))
            sys.exit()

    def add_user(user, password, auth):
        try:
            with open('../data/users.json', 'r') as users:
                auth.user_table = json.load(users)
                users.close()
            os.mkdir('../data/' + user)
            auth.add_user(user, password, '../data/' + user, perm='rwl')
            with open('../data/users.json', 'w') as users:
                json.dump(auth.user_table, users)
                users.close()
        except Exception as e:
            print('Failed to add user:\n' + str(e))


s = Server()
s.startServer()
