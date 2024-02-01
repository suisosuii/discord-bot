# ベースイメージとして公式のPython 3.10イメージを使用
FROM python:3.10

# 作業ディレクトリを設定
WORKDIR /app

# 環境変数を設定して、Pythonが.pycファイルをコンテナに書き込まないようにする
ENV PYTHONDONTWRITEBYTECODE 1
# 環境変数を設定して、Pythonが標準入力をバッファリングしないようにする
ENV PYTHONUNBUFFERED 1

# Poetryをインストール
RUN pip install poetry

# 依存関係をコピーしてインストール
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-dev

# アプリケーションをコピー
COPY . .

# アプリケーションを実行
CMD ["python", "main.py"]

