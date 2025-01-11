FROM python:3.12

WORKDIR /usr/src/app

RUN curl -sSL https://install.python-poetry.org | python3 - && \
ln -s /root/.local/bin/poetry /usr/local/bin/poetry

COPY ./pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --without=dev

COPY ./app .

COPY ./entrypoint.sh ./

CMD bash entrypoint.sh
