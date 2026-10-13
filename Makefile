.PHONY: build build-deps test runserver

IMAGE ?= dumpstermap-backend
PORT ?= 8000

build:
	docker build -t $(IMAGE) .

build-deps:
	docker build --target deps -t $(IMAGE)-deps .

test: build-deps
	docker run --rm -v "$(CURDIR)":/app $(IMAGE)-deps pytest -p no:cacheprovider $(ARGS)

DEV_ENV = -e DEBUG=True -e SECRET_KEY=insecure-dev-key
DOCKER_CMD = docker run --rm $(DEV_ENV) -v "$(CURDIR)":/app

migrate: build-deps
	$(DOCKER_CMD) $(IMAGE)-deps python manage.py migrate

runserver: build-deps migrate
	$(DOCKER_CMD) -p $(PORT):8000 $(IMAGE)-deps python manage.py runserver 0.0.0.0:8000
