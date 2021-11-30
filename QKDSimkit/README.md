# Instructions

How to set up the server and run the client with a default configuration

## Server


### Installing
* Create a conda environment (optional but recommended)
```
$ conda create -n Quantumacy python=3.8.10
$ conda activate Quantumacy
```

* install requirements
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


### Executing

* Run with the most basic configuration: channel will run on the same machine as the server and 
```
$ QKDSimkit server local 
```

* Run with custom channel settings (noise, eavesdropper)
```
$ QKDSimkit server local -n 0.5 -e True
```

* Run server using an external channel
```
$ QKDSimkit server -a [host:port] external -ca [host:port]
```

### Help

For more options please check
```
$ QKDSimkit server -h
$ QKDSimkit server local -h
$ QKDSimkit server external -h
```

##Client

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

### Executing

* Run with the most basic configuration
```
QKDSimkit client [server_host:port] [channel_host:port]
```
* If you want to specify the number of keys use and their size use:
```
QKDSimkit client [server_host:port] [channel_host:port] -n [num_keys] -s [size]
```

### Help

For more options please check
```
python client -h
```

## Authors

Contributor names and contact info:

Alberto Di Meglio

Gabriele Morello [[email]](mailto:gabriele.morello@cern.ch)

## License

This project is licensed under the MIT License - see the LICENSE file for details

## Version History
* 
* 0.0.1
    * Initial Release
    

## Acknowledgments

