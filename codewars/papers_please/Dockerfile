FROM python:3.7

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY /papers_please /papers_please

WORKDIR /papers_please

ENTRYPOINT ["python"]