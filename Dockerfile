FROM python:3.10.1-slim-buster AS base

LABEL maintainer="somespecialone <tkachenkodmitriy@yahoo.com>"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

FROM base AS builder

WORKDIR /usr/workspace/

ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

ENV POETRY_HOME="/.poetry" \
    POETRY_VERSION=1.1.12 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true

ENV PATH="$POETRY_HOME/bin:/.venv/bin:$PATH"

RUN apt-get update && apt-get install --no-install-recommends -y git curl
RUN curl -sSL "https://install.python-poetry.org" | python -

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install --no-interaction --no-root --no-dev

FROM base AS clever-inspect

LABEL description="CSGO items inspect service"

COPY --from=builder /usr/workspace/.venv /usr/workspace/.venv
ENV PATH="/usr/workspace/.venv/bin:$PATH"

WORKDIR /usr/workspace/inspect

RUN touch cred.json
COPY . .

VOLUME [ "/usr/workspace/inspect/data" ]

EXPOSE 8000

HEALTHCHECK --interval=2m --timeout=5s --retries=3 CMD [ "./docker-healthcheck.sh" ]

ENTRYPOINT [ "./docker-entrypoint.sh" ]
