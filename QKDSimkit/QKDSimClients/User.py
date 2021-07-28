import os
import json
import sys
from utils import encrypt_file, decrypt_file
from QKD_Bob import import_key
from ftplib import FTP


class Client(object):
    def __init__(self, username, password):
        self.dest_path = ''
        self.file_list = []
        s = json.load(open('../config.json', ))['Server']
        try:
            print('Connecting to Server: ')
            self.ftp = FTP(s['host'])
        except Exception as e:
            print('FTP error:\n' + str(e))
            sys.exit()

        self.ftp.set_debuglevel(1)

        try:
            self.ftp.login(username, password)
        except Exception as e:
            print('Wrong username or password:\n' + str(e))
            sys.exit()

        print("logged")

        try:
            bits = import_key()
            self.key = [int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8)]
            self.key = bytearray(self.key)[:32]
            print(len(self.key))
            print("Key:" + str(self.key))
        except Exception as e:
            print('Failed to retrieve symmetric key:\n' + str(e))
            sys.exit()

    def send(self, source_path):
        try:
            for file in os.listdir(source_path):
                try:
                    print("Encrypting " + file)
                    encrypt_file(self.key, source_path + file)
                except Exception as e:
                    print('encryption failed:\n' + str(e))
                    sys.exit()

                localfile = open(source_path + file + '.enc', "rb")

                try:
                    print("[!] File Transfer in Progress....")
                    print()
                    result = self.ftp.storbinary("STOR " + file + '.enc', localfile)

                    os.remove(source_path + file + '.enc')
                except Exception as e:
                    print('Transfer failed:\n' + str(e))
                    sys.exit()

                else:
                    print(str(result))
        except Exception as e:
            print("Failed to retrieve file to send:\n" + str(e))
            sys.exit()

    def retrieve(self, file, dest_path):
        try:
            print("[!] File Transfer in Progress....")
            with open(dest_path + file + '.enc', 'wb') as out_file:
                result = self.ftp.retrbinary("RETR " + file, out_file.write)
                print(str(result))
        except Exception as e:
            print('Transfer failed:\n' + str(e))
            sys.exit()

        try:
            decrypt_file(self.key, dest_path + file + '.enc')
            os.remove(dest_path + file + '.enc')
        except Exception as e:
            print('Decryption failed:\n' + str(e))
            sys.exit()

    def callback_retrieve_list(self, line):
        file = line.rsplit(' ', 1)[1]
        self.file_list.append(file)

    def retrieve_all(self, dest_path):
        self.dest_path = dest_path
        self.ftp.retrlines("LIST ", self.callback_retrieve_list)
        for file in self.file_list:
            self.retrieve(file, self.dest_path)


    def close(self):
        self.ftp.quit()


if __name__ == '__main__':
    c = Client('user0', '12345')
    c.send('../data/client0_img/')
    for f in os.listdir('../data/client0_img'):
        os.remove(os.path.join('../data/client0_img', f))
    c.retrieve_all('../data/client0_img/')
    #c.retrieve('file1.jpeg', '../data/client0_img/')
    c.close()
else:
    c = Client(sys.argv[1], sys.argv[2])
