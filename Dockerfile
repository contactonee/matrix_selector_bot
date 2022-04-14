FROM continuumio/miniconda3

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app app
WORKDIR app

ENTRYPOINT python main.py --token ${BOT_TOKEN}