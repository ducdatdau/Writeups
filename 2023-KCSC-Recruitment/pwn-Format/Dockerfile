FROM ubuntu:22.04

MAINTAINER anonymous
RUN apt-get update

RUN useradd -m format

RUN apt-get update --fix-missing -y

RUN apt-get install -y apt-utils software-properties-common

RUN apt-get install -y build-essential \
        socat \
        netcat 

ADD ./flag /home/format
ADD ./format /home/format

ENTRYPOINT ["sh", "-c", "exec socat -s TCP-LISTEN:1337,reuseaddr,fork EXEC:/home/format/format,stderr"]
EXPOSE 1337
