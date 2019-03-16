if [ -t 1 ]
    then
        docker run -it --rm --user $(id -u):$(id -g) -v `pwd`:/usr/data svgwrite:local python -B $1
else
    docker run --rm --user $(id -u):$(id -g) -v `pwd`:/usr/data svgwrite:local python -B $1
fi
