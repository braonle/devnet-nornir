FROM python:3

ADD config/* /nornir/config/
ADD main.py /nornir/
ADD requirements.txt /nornir

WORKDIR /nornir

RUN pip3 install -r requirements.txt

CMD ["python", "./main.py", "ca02.15c8.0008"]
