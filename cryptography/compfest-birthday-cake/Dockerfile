FROM ubuntu:18.04
RUN apt-get update && apt-get -y install python3 socat python3-pip
COPY app.py ./
COPY key.txt ./
COPY pass.txt ./
COPY requirements.txt ./
RUN pip3 install -r requirements.txt
ENV HOST 0.0.0.0
ENV PORT 5432
EXPOSE 5432

CMD socat TCP-LISTEN:5432,reuseaddr,fork EXEC:"python3 prob.py"
