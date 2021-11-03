import http.client
import urllib.parse
from QKDSimkit.QKDSimClients.utils import hash_token, decrypt
from QKDSimkit.QKDSimClients.QKD_Bob import import_key


def get_key(token, number, size):
    hashed = hash_token(token)
    params = urllib.parse.urlencode({'hashed': hashed})
    conn = http.client.HTTPConnection("127.0.0.1:5002")
    conn.request("GET", "/hello?" + params)
    r = conn.getresponse()
    if r.status != 200:
        return r.status
    data = r.read().decode()
    proof = decrypt(token, data)
    conn.close()
    hash_proof = hash_token(proof)
    params = urllib.parse.urlencode({'number': number, 'size': size, 'hashed': hashed, 'hash_proof': hash_proof})
    conn.close()
    conn1 = http.client.HTTPConnection("127.0.0.1:5002")
    conn1.request("GET", "/proof?" + params)
    r = conn1.getresponse()
    if r.status == 200:
        key_list = []
        for n in range(number):
            key_list.append(import_key(ID=hashed, size=size))
        return key_list
    else:
        return r.status


if __name__ == '__main__':
    l = get_key('7KHuKtJ1ZsV21DknPbcsOZIXfmH1_MnKdOIGymsQ5aA=', 1, 256)
    print(l)
