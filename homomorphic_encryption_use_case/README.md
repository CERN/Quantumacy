# Quantumacy Homomorphic Encryption Use Cases

This use case makes use of three different services to create a post-quantum secure data analysis pipeline. Data is encrypted at rest (HE), in transit (HE + QKD) and in processing (HE).



## Requirements and Dependencies

The project makes use of the following libraries and dependencies:
- Docker (Installed)
- Lattigo: Golang library for homomorphic encryption.
- Flask: Python web servers
- NPYIO: Golang interaction with NumPy files.

## Architecture Overview

There are three services to be deployed for the use case: Server, Storage and Client.

The Client Server is deployed in client premises. It is in charge of encrypting the images and keeping the secret key. It generates a key, encrypts the information and sends it over to the storage server. Note that, for the production use case, and to avoid big network transfers, we omit the key generation, since transferring the galois keys introduce a big network delay.

The Storage Server keeps the encrypted information. Whenever a request from the Server is received for processing, it will hand over the encrypted files for the client and wait to receive the results.

The Processing Server acts upon a Client request. It fetches the Storage server for the encrypted information, performs the processing and returns the result to the Storage server.


## Configuration Setup

This project is meant to work distributed, therefore, we expect to have *three* different copies of the repository in three different IP addresses. It can also be run within the same machine, but for simplicity purposes we will assume there exist three different copies of the folders.

For each of the services, in the file `src/python/config.py`, you must set the appropriate IP addresses, and if desired, change the ports accordingly. These will correspond to the placement where the different services will be deployed. 

Also, if the use of QKD is desired together with QKDSimkit, the file `src/python/qkd_config.py` must be filled by setting `QKD_ENABLE = True` and uncommenting the appropriate line for `ROLE`, according to the placement of the QKDSimkit role. If our machine is `ALICE`, we will set `ROLE = SERVER_ROLE` and if our machine is acting as `BOB`, we will set `ROLE = CLIENT_ROLE`. 

## Installation Guide.
The installation makes use of Python, Golang and Flask. For simplicity in the deployment and compilation procedure, we provide a Dockerfiles for the different entities. The only step where there must be involvment is in setting the configuration file as it was explained in the previous section.

### Client Installation

``` 
cd docker
make build_client
```

If the same port mapping (port 7000 for the client) is kept, the client can be run as:

```
make he_client
```

### Storage Installation

``` 
cd docker
make build_storage
```

If the same port mapping (port 7001 for the storage) is kept, the storage server can be run as:

```
make he_storage
```

### Processing Server Installation

``` 
cd docker
make build_server
```

If the same port mapping (port 7002 for the server) is kept, the server can be run as:

```
make he_server
```

## Authors
[José Cabrero-Holgueras](https://jcabrero.github.io/)
