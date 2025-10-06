#!/bin/sh

docker build -t "challenge" . --network=host && docker run -d -p "0.0.0.0:3002:3002" --cap-add=SYS_PTRACE challenge