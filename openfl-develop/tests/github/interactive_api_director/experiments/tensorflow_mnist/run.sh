cd director
bash start_director.sh &

sleep 3
cd ../envoy
python3 shard_descriptor.py &

sleep 2
cd ../../../../../..
python3 -m tests.github.interactive_api_director.experiments.tensorflow_mnist.experiment
