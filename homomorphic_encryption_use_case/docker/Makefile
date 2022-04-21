# ----------------------------------------------------------------------------
# Created By  : José Cabrero-Holgueras
# Created Date: 01/2022
# Copyright: CERN
# License: MIT
# version ='1.0'
# ---------------------------------------------------------------------------

all: kill build run clean
.PHONY: jupygoat

		
build: build_server build_client build_storage

build_base:
	docker build --network=host \
	--build-arg UID=$(shell id -u) --build-arg GID=$(shell id -g) \
	--build-arg USER=$(shell id -u --name) --build-arg GROUP=$(shell id -g --name) \
	-f Dockerfile -t jcabrero/he_quantumacy_base ..

build_server: build_base
	docker build --network=host \
	--build-arg UID=$(shell id -u) --build-arg GID=$(shell id -g) \
	--build-arg USER=$(shell id -u --name) --build-arg GROUP=$(shell id -g --name) \
	-f Dockerfile_Server -t jcabrero/he_quantumacy_server ..

build_client: build_base
	docker build --network=host \
	--build-arg UID=$(shell id -u) --build-arg GID=$(shell id -g) \
	--build-arg USER=$(shell id -u --name) --build-arg GROUP=$(shell id -g --name) \
	-f Dockerfile_Client -t jcabrero/he_quantumacy_client ..

build_storage: build_base
	docker build --network=host \
	--build-arg UID=$(shell id -u) --build-arg GID=$(shell id -g) \
	--build-arg USER=$(shell id -u --name) --build-arg GROUP=$(shell id -g --name) \
	-f Dockerfile_Storage -t jcabrero/he_quantumacy_storage ..

he_server:
	docker run  \
		--net host \
		--publish 7002:7002 -d \
		--hostname=$@ --name=$@ \
		--rm \
		jcabrero/he_quantumacy_server

he_client:
	docker run  \
		--net host \
		--publish 7000:7000 -d \
		--hostname=$@ --name=$@ \
		--rm \
		jcabrero/he_quantumacy_client

he_storage:
	docker run  \
		--net host -it --rm \
		--publish 7001:7001 -d \
		--hostname=$@ --name=$@ \
		--rm \
		jcabrero/he_quantumacy_storage

test:
	docker run  \
		--net host \
		--hostname=$@ --name=$@ \
		-it --rm -v $(shell pwd)/../:/home/jocabrer/mnt \
		jcabrero/he_quantumacy_base \
		bash -c "cd mnt/src && python3 test/test.py 10"

test_docker:
	docker run  \
		--net host \
		--hostname=$@ --name=$@ \
		-it --rm -v $(shell pwd)/../:/home/jocabrer/mnt \
		jcabrero/he_quantumacy_base

client: build_client he_client

server: build_server he_server

storage: build_storage he_storage

run: he_server he_client he_storage

clean:
	docker rmi $(shell docker images --filter dangling=true -q --no-trunc) || true

kill:
	docker kill he_client he_server he_storage  || true

