import struct
import os
import random

from Crypto.Cipher import AES
from QKD_Bob import code

path = 'C:\\Users\\sgabb\\repos\\Quantumacy\\QKDSimkit\\QKDSimClients\\'

def encrypt_file(key, in_filename, out_filename):
    with open(in_filename, 'rb') as infile:
        chunk = infile.read()
        cipher = AES.new(key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(chunk)
        with open(out_filename, 'wb') as file_out:
            [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
            file_out.close()
            print(file)

bits = code()
key = [int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8)][:16]
key = bytearray(key)
print("Key:")
print(key)
print("Encrypting: ")
for file in os.listdir(path + 'source'):
    encrypt_file(key, path + 'source\\' + file, path + 'mid\\' + file)

