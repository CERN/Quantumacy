import os
import json
import sys
from utils import encrypt_file, decrypt_file
from QKD_Bob import import_key
from ftplib import FTP


class Client(object):
    """Client class for FTP"""
    def __init__(self, username, password):
        """Set up user

        After connecting and logging in it exchanges the symmetric key with the FTP server
        """
        self.dest_path = ''
        self.file_list = []
        s = json.load(open('../config.json', ))['Server']
        try:
            print('Connecting to Server: ')
            self.ftp = FTP()
            self.ftp.connect(s['host'], s['port'])
        except Exception as e:
            print('FTP error:\n' + str(e))
            sys.exit()

        self.ftp.set_debuglevel(1)

        try:
            self.ftp.login(username, password)
        except Exception as e:
            print('Wrong username or password:\n' + str(e))
            sys.exit()

        try:
            bits = import_key()
            self.key = [int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8)]
            self.key = bytearray(self.key)[:32]
        except Exception as e:
            print('Failed to retrieve symmetric key:\n' + str(e))
            sys.exit()

    def send(self, file: str, source_path: str):
        """Send a file to FTP server

        Encrypt file, send the encrypted file and remove the encrypted copy,
        Args:
            file (str): filename
            source_path (str): path to file to send
        """
        try:
            print("Encrypting " + file)
            encrypt_file(self.key, source_path + file)
        except Exception as e:
            print('encryption failed:\n' + str(e))
            sys.exit()
        try:
            with open(source_path + file + '.enc', "rb") as localfile:
                print("[!] File Transfer in Progress....")
                self.ftp.storbinary("STOR " + file + '.enc', localfile)
        except Exception as e:
            print('Transfer failed:\n' + str(e))
            sys.exit()
        finally:
            try:
                os.remove(source_path + file + '.enc')
            except FileNotFoundError:
                print('File not found')
                pass

    def send_all(self, source_path):
        """Send every file in a directory to FTP server

        for every file in the given directory it calls the send method
        Args:
            source_path (str):
        """
        try:
            for file in os.listdir(source_path):
                self.send(file, source_path)
        except Exception as e:
            print("Failed to send or to encrypt:\n" + str(e))
            sys.exit()

    def retrieve(self, file: str, dest_path: str):
        """Retrieve a single from FTP server

        Retrieve file from server, decrypt it and remove the encrypted copy
        Args:
            file (str): filename
            dest_path (str): path to destination directory for retrieved file
        """
        try:
            print("[!] File Transfer in Progress....")
            with open(dest_path + file + '.enc', 'wb') as out_file:
                self.ftp.retrbinary("RETR " + file, out_file.write)
        except Exception as e:
            print('Transfer failed:\n' + str(e))
            sys.exit()
        try:
            decrypt_file(self.key, dest_path + file + '.enc')
        except Exception as e:
            print('Decryption failed:\n' + str(e))
            sys.exit()
        finally:
            try:
                os.remove(dest_path + file + '.enc')
            except FileNotFoundError:
                print('File not found')
                pass

    def callback_retrieve_list(self, line):
        file = str(line.rsplit(' ', 1)[1])
        self.file_list.append(file)

    def retrieve_all(self, dest_path: str):
        """Retrieve all files in the home directory of the FTP server for this user
        Args:
            dest_path (str): path to destination directory for retrieved file
        """
        try:
            self.dest_path = dest_path
            self.ftp.retrlines("LIST ", self.callback_retrieve_list)
            for file in self.file_list:
                self.retrieve(file, self.dest_path)
        except Exception as e:
            print("Failed to list directory\n" + str(e))
            sys.exit()

    def close(self):
        self.ftp.quit()


if __name__ == '__main__':
    c = Client('admin', 'admin')
    c.send_all('../data/client0_img/')
    """for f in os.listdir('../data/client0_img'):
        os.remove(os.path.join('../data/client0_img', f))
    c.retrieve_all('../data/client0_img/')
    c.retrieve('file1.jpeg', '../data/client0_img/')"""
    c.close()
