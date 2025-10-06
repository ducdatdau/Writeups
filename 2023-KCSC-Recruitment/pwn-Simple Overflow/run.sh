#!/bin/bash

docker build -t simple_overflow .

docker run -p 1337:1337 -it simple_overflow /bin/bash