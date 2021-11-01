import http.client
import json
import hashlib
import urllib.parse
from QKDSimkit.QKDSimClients.utils import hash_token
from QKDSimkit.QKDSimClients.QKD_Bob import import_key


def get_key(token, number, size):
    hashed = hash_token(token)
    params = urllib.parse.urlencode({'number': number, 'size': size, 'ID': hashed})
    conn = http.client.HTTPConnection("127.0.0.1:8003")
    conn.request("GET", "/signal?" + params)
    r = conn.getresponse()
    if r.status == 200:
        key_list = []
        for n in range(number):
            key_list.append(import_key(ID=hashed, password=token, size=size))
        return key_list
    else:
        return r.status

if __name__ == '__main__':
    l = get_key('7KHuKtJ1ZsV21DknPbcsOZIXfmH1_MnKdOIGymsQ5aA=', 1, 256)
    print(l)
