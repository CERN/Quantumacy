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
        """Decrypt a received file, automatically called for each received file"""
        try:
            print('Decrypting: ' + filename)
            decrypt_file(self.key, filename)
            os.remove(filename)
        except Exception as e:
            print('Failed to handle received file\n' + str(e))
        finally:
            try:
                os.remove(filename + '.enc')
            except FileNotFoundError:
                print('File not found')
                pass

    def on_login(self, user):
        """Exchange with the user a symmetric key"""
        try:
            bits = import_key()
            self.key = [int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8)]
            self.key = bytearray(self.key)[:32]
        except Exception as e:
            print('Failed to retrieve symmetrical key:\n' + str(e))


    def on_login_failed(self, username, password):
        print(username + " failed to login")

    def ftp_RETR(self, file):
        """Encrypt a file before answering to the RETR command and sending it"""
        try:
            print('Encrypting ' + file)
            encrypt_file(self.key, file)
            print(os.listdir())
            super().ftp_RETR(file + '.enc')
            os.remove(file + '.enc')
        except Exception as e:
            print("Failed to answer RETR\n" + str(e))

class Server(object):
    """Server class (FTP)"""
    def startServer(self):
        """Start server
        prepare and start server
        """
        try:
            authorizer = DummyAuthorizer()
            with open('../data/users.json', 'r') as users:
                authorizer.user_table = json.load(users)
        except Exception as e:
            print("Failed to load user table (may be a permission issue or a duplicate user): \n" + str(e))
            sys.exit()

        try:
            s = json.load(open('../data/config.json', ))['Server']
            handler = MyHandler  # select the created custom FTP handler
            handler.authorizer = authorizer  # assign the authorizer to the handler
            handler.banner = "Server Ready.."  # server banner is returned when the client calls a getWelcomeMessage() call
            address = (s['host'], s['port'])
            server = FTPServer(address, handler)
            server.serve_forever()  # start the server
        except Exception as e:
            print("Server failed to start:\n" + str(e))
            sys.exit()

    def add_user(self, user: str, password: str, auth: object, dir: str):
        """add a user

        add a user to current server's user table and to the stored user table, create a directory that will be used as
        user's home
        Args:
            user (str): username
            password (str): password
            auth (str): authorizer
            dir (str): path to home directory for user
        """
        try:
            with open('../data/users.json', 'r') as users:
                auth.user_table = json.load(users)
                users.close()
            os.mkdir(dir + 'data/' + user)
            auth.add_user(user, password, dir + '/data/' + user, perm='rwl')
            with open('../data/users.json', 'w') as users:
                json.dump(auth.user_table, users)
                users.close()
        except Exception as e:
            print('Failed to add user:\n' + str(e))
            sys.exit()


s = Server()
s.startServer()
