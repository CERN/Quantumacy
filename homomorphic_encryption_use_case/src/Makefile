# ----------------------------------------------------------------------------
# Created By  : José Cabrero-Holgueras
# Created Date: 01/2022
# Copyright: CERN
# License: MIT
# version ='1.0'
# ---------------------------------------------------------------------------

all: build

build:
	go build ./internal/he
	go build -o bin/keygen ./cmd/keygen
	go build -o bin/encryptor ./cmd/encryptor
	go build -o bin/decryptor ./cmd/decryptor
	go build -o bin/runtime ./cmd/runtime
	go build -o bin/simulator ./cmd/simulator


