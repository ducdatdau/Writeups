#!/bin/bash

docker build -t format .

docker run -p 1337:1337 -it format /bin/bash