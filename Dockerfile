FROM continuumio/miniconda3

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /usr/src/app
COPY app .

ENTRYPOINT python main.py