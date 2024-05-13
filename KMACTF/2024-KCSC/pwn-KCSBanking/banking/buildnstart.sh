#!/bin/sh

docker build . -t banking
docker run --rm -p10002:10002 -it banking