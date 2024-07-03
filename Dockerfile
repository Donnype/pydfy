ARG PYTHON_VERSION=3.10
FROM python:$PYTHON_VERSION-slim

ARG USER=pydfy-user

RUN apt-get update && apt-get install -y chromium chromium-driver curl
RUN curl -sLO https://github.com/tailwindlabs/tailwindcss/releases/download/v3.4.3/tailwindcss-linux-x64 && \
    chmod +x tailwindcss-linux-x64 && \
    mv tailwindcss-linux-x64 /usr/local/bin/tailwindcss
RUN groupadd --gid 1000 $USER && adduser --disabled-password --gecos '' --uid 1000 --gid 1000 $USER

USER $USER
WORKDIR /home/$USER/pydfy
ENV PATH="/home/$USER/.local/bin:/home/$USER/pydfy/.venv/bin:${PATH}" \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true\
    PYDFY_OUT=/dev/stdout

RUN --mount=type=cache,target=/root/.cache pip install --user poetry==1.4.2

COPY --chown=$USER:$USER ./pyproject.toml ./poetry.lock ./
RUN --mount=type=cache,target=/root/.cache poetry install --with dev --all-extras

COPY --chown=$USER:$USER ./ ./
RUN --mount=type=cache,target=/root/.cache poetry install --with dev --all-extras

WORKDIR /pydfy
ENTRYPOINT ["python"]
CMD ["main.py"]
