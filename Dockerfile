# ベースイメージとして公式のPython 3.10イメージを使用
FROM python:3.10

WORKDIR /bot
COPY requirements.txt /bot/
RUN pip install -r requirements.txt
COPY . /bot
CMD python main.py
