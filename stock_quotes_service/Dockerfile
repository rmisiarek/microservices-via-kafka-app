FROM python:3.9-slim-buster AS python-base

ENV APP_WORKDIR='/app' \
    # Python:
    PYTHONFAULTHANDLER=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # Pip:
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # Poetry:
    POETRY_VERSION=1.1.8 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME="/opt/poetry" \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Stage 'builder-base' is for build required dependencies
FROM python-base AS builder-base

# Upgrade & install dependencies and then clean cache
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential \
    && apt-get clean

# Install 'Poetry' package manager to $POETRY_HOME path
# with version equal to $POETRY_VERSION
RUN curl -sSL 'https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py' | python \
  && poetry --version

# Copy Python requirements to use Docker cache
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./

# Install project
RUN poetry install --no-dev --no-ansi \
    && rm -rf $POETRY_CACHE_DIR

# Copy source code
COPY . $APP_WORKDIR

# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
# Here can be development stage, for example to run bandit, pytest and so on
# --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

# Stage 'production' with only required (runtime) dependencies
FROM python-base AS production

WORKDIR $APP_WORKDIR

# Create 'web' group and 'web' user & set correct permissions
RUN groupadd -r web \
    && useradd -d $APP_WORKDIR -r -g web web \
    && chown web:web -R $APP_WORKDIR

COPY --from=builder-base --chown=web:web $VENV_PATH $VENV_PATH
COPY --from=builder-base --chown=web:web $APP_WORKDIR .

# Use not root user!
USER web

CMD ["python", "stock_quotes_service.py"]
