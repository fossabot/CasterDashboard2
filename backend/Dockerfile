FROM python:3.9

# Install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
RUN /root/.poetry/bin/poetry config virtualenvs.in-project true

# Install dependencies
WORKDIR /backend
COPY pyproject.toml .
RUN /root/.poetry/bin/poetry install
COPY src src
COPY .env.docker .env
COPY docker-start.sh .