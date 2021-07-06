import struct

from Crypto.Cipher import AES
import time
import os
from QKD_Alice import code

path = 'C:\\Users\\sgabb\\repos\\Quantumacy\\QKDSimkit\\QKDSimClients\\'

def decrypt_file(key, in_filename, out_filename):
    with open(in_filename, 'rb') as file_in:
        nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        with open(out_filename, 'wb') as file_out:
            file_out.write(data)
            file_out.close()
            print(file)

bits = code()
key = [int("".join(map(str, bits[i:i + 8])), 2) for i in range(0, len(bits), 8)][:16]
key = bytearray(key)

print(key)

time.sleep(2)
print("Decrypting: ")
for file in os.listdir(path + 'mid'):
    decrypt_file(key, path + 'mid\\' + file, path + 'dest\\' + file)

