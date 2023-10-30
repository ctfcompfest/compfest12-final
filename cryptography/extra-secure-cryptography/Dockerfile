FROM python:3.8-slim-buster

RUN useradd --create-home --shell /bin/bash compfest12
RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y gcc
RUN apt-get install -y socat
RUN pip install pycryptodome

COPY build/* /home/compfest12/

RUN chmod 555 /home/compfest12/soal.py
RUN chmod 444 /home/compfest12/flag.txt

USER compfest12
WORKDIR /home/compfest12

USER compfest12

CMD /usr/bin/socat TCP-LISTEN:1337,reuseaddr,fork EXEC:"./soal.py" && fg