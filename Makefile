SHELL := bash
.ONESHELL:
.SHELLFLAGS := -eu -o pipefail -c
.PHONY: build

export DOCKER_BUILDKIT=1

check:
	poetry run pre-commit run --all --color always

build:
	poetry build

utest:
	docker build . -t pydfy:latest
	docker run --rm pydfy -m pytest
