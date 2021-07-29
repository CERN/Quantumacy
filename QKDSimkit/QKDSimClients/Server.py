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


class MyHandler(FTPHandler):  # FTP server handler
    def on_file_received(self, filename):  # Once the file is received by the server, trigger this event
        print('Decrypting: ' + filename)
        decrypt_file(self.key, filename)
        os.remove(filename)

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
        print('Encrypting ' + file)
        encrypt_file(self.key, file)
        print(os.listdir())
        super().ftp_RETR(file + '.enc')
        os.remove(file + '.enc')


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
        with open('../data/users.json', 'r') as users:
            auth.user_table = json.load(users)
            users.close()
        os.mkdir('../data/' + user)
        auth.add_user(user, password, '../data/' + user, perm='rwl')
        with open('../data/users.json', 'w') as users:
            json.dump(auth.user_table, users)
            users.close()


s = Server()
s.startServer()
