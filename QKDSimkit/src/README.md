# Server-client interface

How to set up the server and run the client with a default configuration

## Server


### Installing
* Create a conda environment
```
$ conda create -n Quantumacy python=3.8.10
$ conda activate Quantumacy
```

* install requirements
```
$ pip install -r ../requirements.txt
```

* Download, install and run Redis 
```
$ wget https://download.redis.io/releases/redis-6.2.6.tar.gz
$ tar xzf redis-6.2.6.tar.gz
$ cd redis-6.2.6
$ make
$ src/redis-server
```


### Executing program

* Run with the most basic configuration: channel will run on the same machine as the server and 
```
python Server.py l 
```

* Run with personalized channel settings (noise, eavesdropper)
```
python Server.py l -n 0.5 -e True
```

* Run server and use an external channel
```
python Server.py --host [host] --port [port] ca [host:port]
```

### Help

For more options please check
```
python Server.py -h
python Server.py l -h
python Server.py ca -h
```

##Client

### Installing

* Create a conda environment
```
$ conda create -n Quantumacy python=3.8.10
$ conda activate Quantumacy
```
* install requirements
```
$ pip install -r ../requirements.txt
```
### Executing program

* Run with the most basic configuration
```
python Client.py [server_host:port] [channel_host:port]
```
* If you want to specify the number of keys use and their size use:
```
python Client.py [server_host:port] [channel_host:port] -n [num_keys] -s [size]
```

### Help

For more options please check
```
python Client.py -h
```

## Authors

Contributors names and contact info:

[Gabriele Morello](https://www.linkedin.com/in/gabriele-morello/)

## Version History

* 0.1
    * Initial Release

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

