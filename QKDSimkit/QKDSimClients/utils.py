import sys
from Crypto.Cipher import AES

def validate(shared_key, other_shared_key):
    if len(shared_key) > 0 and len(shared_key) == len(other_shared_key):
        i = 0
        count = 0
        decision = 0
        while i < len(shared_key):
            if shared_key[i] == other_shared_key[i]:
                count += 1
            i += 1
        return count/len(shared_key)
    else:
        print("Error")
        return -1


def decrypt_file(key, filename: str):
    try:
        with open(filename, 'rb') as file_in:
            nonce, tag, ciphertext = [file_in.read(x) for x in (16, 16, -1)]
        cipher = AES.new(key, AES.MODE_EAX, nonce)
        data = cipher.decrypt_and_verify(ciphertext, tag)
        with open(filename[:-4], 'wb') as file_out:
            file_out.write(data)
            file_out.close()
    except Exception as e:
        print("failed to decrypt:\n" + str(e))
        sys.exit()

def encrypt_file(key, in_filename):
    try:
        with open(in_filename, 'rb') as infile:
            chunk = infile.read()
            try:
                cipher = AES.new(key, AES.MODE_EAX)
                ciphertext, tag = cipher.encrypt_and_digest(chunk)
            except Exception as e:
                print("key or value error: \n" + str(e))
                sys.exit()
            with open(in_filename + '.enc', 'wb') as file_out:
                [file_out.write(x) for x in (cipher.nonce, tag, ciphertext)]
                file_out.close()
    except Exception as e:
        print('IO error during encryption: \n' + str(e))
        sys.exit()
