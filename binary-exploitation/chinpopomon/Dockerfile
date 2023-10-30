FROM ubuntu:20.04

RUN useradd --create-home --shell /bin/bash compfest12
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install socat -y

COPY build/* /home/compfest12/
WORKDIR /home/compfest12/

RUN chmod 555 chinpopomon
RUN chmod 444 flag.txt

USER compfest12

CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"./chinpopomon" && fg