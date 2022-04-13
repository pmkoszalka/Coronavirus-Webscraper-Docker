FROM python:3.9

ENV PYTHONUNBUFFERED=1

COPY . /newfolder

RUN  pip3 install -r /newfolder/requirements.txt

CMD [ "python", "newfolder/run.py" ]