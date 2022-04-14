FROM condaforge/miniforge3

ARG token
COPY app app

conda create --name telegram_bot --file requirements.txt

WORKDIR app
ENTRYPOINT python main.py --token $token