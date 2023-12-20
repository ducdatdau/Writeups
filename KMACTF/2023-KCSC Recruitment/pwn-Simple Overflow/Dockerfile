FROM ubuntu:22.04

MAINTAINER anonymous
RUN apt-get update

RUN useradd -m simple_overflow

RUN apt-get update --fix-missing -y

RUN apt-get install -y apt-utils software-properties-common

RUN apt-get install -y build-essential \
        socat \
        netcat 

WORKDIR /home/simple_overflow

ADD ./flag /home/simple_overflow
ADD ./simple_overflow /home/simple_overflow

ENTRYPOINT ["sh", "-c", "exec socat -s TCP-LISTEN:1337,reuseaddr,fork EXEC:/home/simple_overflow/simple_overflow,stderr"]

EXPOSE 1337

