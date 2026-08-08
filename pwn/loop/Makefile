BUILD_IMAGE=builder:latest
BUILD_OPTS=-std=c99 -no-pie
DOCKER_IMAGE=registry.vuln.si/ptr2026/pwn/loop:latest
DOCKER_OPTS=--platform=linux/amd64

bin:
	gcc -o main main.c ${BUILD_OPTS}

build:
	docker build ${DOCKER_OPTS} -t ${DOCKER_IMAGE} .

push: build
	docker push ${DOCKER_IMAGE}

run: build
	docker run ${DOCKER_OPTS} -p 1337:1337 --rm --name pwn-loop ${DOCKER_IMAGE}

dist:
	zip dist.zip Dockerfile main

install: dist
	ctf challenge install .

sync: dist
	ctf challenge sync .
