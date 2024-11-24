FROM ubuntu:23.04

RUN apt-get update && apt-get install -y socat && apt-get clean && useradd user && mkdir /app
ADD /share/ /app/
RUN chmod +x /app/run.sh /app/banking

USER user
WORKDIR /app
CMD ["/app/run.sh"]