.PHONY: build build-deps build-test test migrate runserver upgrade-deps

IMAGE ?= dumpstermap-backend
PORT ?= 8000

build:
	docker build -t $(IMAGE) .

build-deps:
	docker build --target deps -t $(IMAGE)-deps .

build-test:
	docker build --target test -t $(IMAGE)-test .

test: build-test
	docker run --rm -v "$(CURDIR)":/app $(IMAGE)-test pytest -p no:cacheprovider $(ARGS)

DEV_ENV = -e DEBUG=True -e SECRET_KEY=insecure-dev-key
DOCKER_CMD = docker run --rm $(DEV_ENV) -v "$(CURDIR)":/app

migrate: build-deps
	$(DOCKER_CMD) $(IMAGE)-deps python manage.py migrate

runserver: build-deps migrate
	$(DOCKER_CMD) -p $(PORT):8000 $(IMAGE)-deps python manage.py runserver 0.0.0.0:8000

upgrade-deps:
	# Upgrade all dependencies in uv.lock
	uv lock --upgrade
