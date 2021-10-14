build:
	docker build -t laserloom:local .
run:
	docker run -it --rm --user $(id -u):$(id -g) -v `pwd`:/usr/data laserloom:local python -B $1