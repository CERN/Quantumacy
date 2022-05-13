# Instructions

How to set up the server and run the client with a default configuration

## Server


### Installing
* Create a conda environment (optional but recommended)
```
$ conda create -n Quantumacy python=3.8.10
$ conda activate Quantumacy
```

* Install requirements
```
$ pip install QKDSimkit
```

* Download, install and run Redis 

```
$ wget https://download.redis.io/releases/redis-6.2.6.tar.gz
$ tar xzf redis-6.2.6.tar.gz
$ cd redis-6.2.6
$ make
$ src/redis-server
```
Redis is a requirement for the QKDSimkit server and QKDSimkit p2p

### Executing
* Run the server and the channel on the same machine, it will start both the server and the channel, the default addresses are 127.0.0.1:5002 for the server and 127.0.0.1:5000 for the channel
```
$ QKDSimkit server local
```

* It is possible to run the channel with custom settings adding noise (-n) and simulating an eavesdropper (-e)
```
$ QKDSimkit server local -n 0.5 -e True
```

* In case you want to share an already existing channel with other servers or with a peer to peer infrastructure you can use this command to connect the server to an external channel:
```
$ QKDSimkit server -a [host:port] external -ca [host:port]
```

### Additional commands
* Add a user: specify a token, it can be useful for multiple clients
```
$ QKDSimkit server add_user <token>
```
* Retrieve keys from the server it is possible to specify a token (-t) to retrieve a specific set of keys
```
$ QKDSimkit server retrieve 
```

### Help

For more options please check
```
$ QKDSimkit server -h
$ QKDSimkit server local -h
$ QKDSimkit server external -h
$ QKDSimkit server add_user -h
$ QKDSimkit server retrieve -h
```

## Client

### Installation
* Create a conda environment (optional but recommended)
```
$ conda create -n Quantumacy python=3.8
$ conda activate Quantumacy
```
* Install requirements
```
$ pip install QKDSimkit
```

### Executing

* Run client
```
$ QKDSimkit client [server_host:port] [channel_host:port]
```

* It is possible to specify the number of keys (-n) and their size (-s):
```
$ QKDSimkit client [server_host:port] [channel_host:port] -n [num_keys] -s [size]
```

* To handle multiple clients it is possible to run the client with a pre shared token
```
$ QKDSimkit client -t [token] [server_host:port] [channel_host:port] 
```
* If you are using a token remember to add the same token to the server running on the server machine:
```
$ QKDSimkit server add_user [token]
```

### Help

For more options please check
```
$ python client -h
```

## P2P
The peer to peer mode provides two servers (Alice and Bob) to simulate a synchronous exchange, there are three components: the channel, Alice and Bob

* Use the following command to run the channel, you can use this channel also in the Server-Client architecture and similarly it is possible to use custom settings like noise (-n) and eavesdropper (-e)
```
$ QKDSimkit channel -a [hostname:port]
```
* Run Alice
```
$ QKDSimkit p2p alice -c [channel_address] -a [hostname:port]
```
* Run Bob
```
$ QKDSimkit p2p bob -c [channel_address] -a [hostname:port]
```

* You can use HTTP requests to Alice and Bob to start the exchange and retrieve keys.  
Check http://[address]/docs to access FastAPI documentation and to know more about HTTP request parameters

## Authors

Contributor names and contact info:

Alberto Di Meglio

Gabriele Morello [[email]](mailto:gabriele.morello@cern.ch)

## License

This project is licensed under the MIT License - see the LICENSE file for details

## Version History
* 0.0.6
* 0.0.5
* 0.0.2
* 0.0.1
    * Initial Release
    

## Acknowledgments

