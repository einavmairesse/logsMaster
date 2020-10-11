FROM python:3

RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get -y install python3

COPY . /LogsMaster/
WORKDIR /LogsMaster

RUN pip3 install --no-cache-dir -r requirements.txt

ENV FLASK_APP=/LogsMaster/LogsMasterApp.py
EXPOSE 5000

#CMD ["flask", "run", "--host", "0.0.0.0", "-p", "5000"]
CMD python LogsMasterApp.py