# Server-client interface

How to set up the server and run the client with a default configuration

## Server

### Dependencies

* Tested with python 3.8.10
* A requirements.txt is provided in the parent directory
* Redis
```
pip install -r ../requirements.txt
```
### Installing

* Download, install and run Redis [[link](https://redis.io/download)]

### Executing program

* Run with the most basic configuration: channel will run on the same machine as server
```
python Server.py -l 
```
* Run just server and use an external channel
```
python Server.py -ca [host:port] --host [host] --port [port]
```

##Client

### Dependencies

* Tested with python 3.8.10
* A requirements.txt is provided in the parent directory
```
pip install -r ../requirements.txt
```
please note that some dependencies are not required if you want to run only the client

### Installing

* Download install and run Redis [[link](https://redis.io/download)]
* Any modifications needed to be made to files/folders

### Executing program

* Run with the most basic configuration
```
python Client.py [server_host:port] [channel_host:port]
```
* If you want to specify the number of keys use and their size use:
```
python Client.py [server_host:port] [channel_host:port] -n [num_keys] -s [size]
```

## Help

Any advise for common problems or issues.
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

