BUILD_IMAGE=builder:latest
BUILD_OPTS=-std=c99
DOCKER_IMAGE=registry.vuln.si/ptr2026/crypto/pki:latest
DOCKER_OPTS=--platform=linux/amd64

bin:

build:
	docker build ${DOCKER_OPTS} -t ${DOCKER_IMAGE} .

push: build
	docker push ${DOCKER_IMAGE}

run: build
	docker run ${DOCKER_OPTS} -p 1337:1337 --rm --name crypto-pki ${DOCKER_IMAGE}

dist:
	zip dist.zip Dockerfile pki.py

install: dist
	ctf challenge install .

sync: dist
	ctf challenge sync .
