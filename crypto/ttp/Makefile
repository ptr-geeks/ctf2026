BUILD_IMAGE=builder:latest
BUILD_OPTS=-std=c99

bin:

build:

push: build

run: build
	./main

dist:
	zip dist.zip ttp.py output.txt

install: dist
	ctf challenge install .

sync: dist
	ctf challenge sync .
