FROM python:3.12.4-slim
WORKDIR /app
COPY ./pyproject.toml* ./
RUN pip install poetry
RUN poetry config virtualenvs.in-project true
RUN poetry install
