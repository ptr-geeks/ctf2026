BUILD_IMAGE=builder:latest
BUILD_OPTS=-std=c99
DOCKER_IMAGE=registry.vuln.si/ptr2026/crypto/qbox:latest
DOCKER_OPTS=--platform=linux/amd64

bin:
	gcc -o main main.c ${BUILD_OPTS}

build:
	docker build ${DOCKER_OPTS} -t ${DOCKER_IMAGE} .

push: build
	docker push ${DOCKER_IMAGE}

run: build
	docker run ${DOCKER_OPTS} -p 1337:1337 --rm --name crypto-qbox ${DOCKER_IMAGE}

dist:

install: dist
	ctf challenge install .

sync: dist
	ctf challenge sync .
