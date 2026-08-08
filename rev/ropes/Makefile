BUILD_IMAGE=builder:latest
BUILD_OPTS=-std=c99

bin:
	docker run \
		${DOCKER_OPTS} --rm -v $(PWD):/app -w /app ${BUILD_IMAGE} \
		gcc -o main main.c ${BUILD_OPTS}

build:

push: build

run: build
	./main

dist:
	zip dist.zip Dockerfile main

install: dist
	ctf challenge install .

sync: dist
	ctf challenge sync .
