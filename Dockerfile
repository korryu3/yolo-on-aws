FROM python:3.12-slim-trixie
# COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /backend
COPY ./pyproject.toml ./
# Fargate内でuvが使えない(バイナリがあってない？)ので、通常のpipインストールに変更
RUN pip install --no-cache-dir .

COPY ./backend /backend

EXPOSE 8080

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
