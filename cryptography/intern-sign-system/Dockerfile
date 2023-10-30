FROM ubuntu:18.04
RUN apt-get update && apt-get -y install python3 socat python3-pip
RUN pip3 install pycryptodome
COPY prob.py ./
COPY flag.txt ./
EXPOSE 3000
CMD socat TCP-LISTEN:3000,reuseaddr,fork EXEC:"python3 prob.py"
