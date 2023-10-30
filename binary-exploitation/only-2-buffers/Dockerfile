FROM ubuntu:20.04

RUN useradd --create-home --shell /bin/bash compfest12
RUN useradd --create-home --shell /bin/bash flag
RUN apt-get update -y && apt-get upgrade -y
# RUN apt-get install socat -y
RUN apt-get install -y --no-install-recommends xinetd

COPY build/files/* /home/compfest12/
COPY build/flag/* /home/flag/

RUN chmod 555 /home/compfest12/
RUN chmod 555 /home/flag/
RUN chmod 400 /home/flag/flag.txt && chmod 555 /home/flag/readFlag
RUN chown flag:flag /home/flag/flag.txt && chown flag:flag /home/flag/readFlag
RUN chmod +s /home/flag/readFlag

WORKDIR /home/compfest12
USER compfest12

CMD ["xinetd", "-dontfork"]
# CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"./only-2-buffers" && fg