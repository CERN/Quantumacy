#How to run a modified version of Openfl using QKD

###Conda environment
Optional
```
conda create -n openfl python=3.8.12
conda activate openfl
```
 
###Redis
Needed to run peer to peer servers
```
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
src/redis-server
```

##QKD Servers:
There are three components it is advised to run channel and alice on the same machine while bob should run on a second machine  

First machine: (Director)
```
pip install —upgrade QKDSimkit
QKDSimkit channel -a <hostname_1>:8000
```
```
QKDSimkit p2p alice -c 127.0.0.1:8000 -a 127.0.0.1:5001
 ```
Other machines: (Collaborators)
```
QKDSimkit p2p bob -c <hostname_1>:8000 -a 127.0.0.1:5003
 ```

##Openfl
Install Openfl on every machine 
```
git clone https://github.com/CERN/Quantumacy.git
cd Quantumacy/openfl-develop
pip install .
```
Move the dataset inside Quantumacy/openfl-develop/Tensorflow_Park/envoy_folder/data  
(Optional): move the dataset inside Quantumacy/openfl-develop/Tensorflow_Park/envoy_folder_2/data in case you want to use two envoys
  
You should run the director on the same machine as the alice component and the collaborator on bob's machine  
In case you want to start more than one collaborator on different machines you should also have a bob process on each machine

###Director:
On Alice machine
```
cd Quantumacy/openfl-develop/Tensorflow_Park/director_folder
fx director start --disable-tls -c director_config.yaml
```


###Collaborator 1:
On Bob machine
```
cd Quantumacy/openfl-develop/Tensorflow_Park/envoy_folder
fx envoy start -n env_one --disable-tls --shard-config-path shard_config_one.yaml -dh <hostname> -dp 3000
```

###(Optional) Collaborator 2:
On Bob machine (it may be a second Bob machine or the same as the first collaborator)
```
cd Quantumacy/openfl-develop/Tensorflow_Park/envoy_folder_2
fx envoy start -n env_two --disable-tls --shard-config-path shard_config_two.yaml -dh <hostname> -dp 3000
```

###Python script
To start the training execute this on a collaborator machine
```
cd Quantumacy/openfl-develop/Tensorflow_Park/workspace
python script_park.py
```

###Note
If the fx execution doesn't work, you may try to use 
```
python ../../openfl/interface/cli.py <rest of the command>
```
instead of fx