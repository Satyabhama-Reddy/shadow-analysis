FROM ubuntu:latest
# COPY view.py /view.py
# COPY runner.sh /runner.sh
# COPY requirements.txt /requirements.txt
COPY . /

RUN apt-get update
RUN apt install -y python3 python3-pip
RUN pip3 --version
RUN pip3 install -r requirements.txt
RUN chmod 700 /runner.sh

EXPOSE 5000

CMD ["./runner.sh"]