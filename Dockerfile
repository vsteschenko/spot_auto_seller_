FROM python:3.11-alpine as python-base

# https://python-poetry.org/docs#ci-recommendations
ENV POETRY_VERSION=1.5.1
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
# Keep Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turn off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# where to place poetry cache and virtual environment
ENV POETRY_CACHE_DIR=/opt/.cache

# stage for Poetry installation
FROM python-base as poetry-base

# Creating a virtual environment just for poetry and install it with pip
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# stage from the base python image
FROM python-base as bot-app

# Copy Poetry to bot-app image
COPY --from=poetry-base ${POETRY_VENV} ${POETRY_VENV}

# Add Poetry to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

# Copy Dependencies
COPY poetry.lock pyproject.toml ./spot_auto_seller/

#set working directory
WORKDIR /spot_auto_seller

# [OPTIONAL] Validate the project is properly configured
RUN poetry check

# Install Dependencies with --no-root
RUN poetry install --no-root --no-interaction --no-cache

# Copy Application
COPY . .

#run the application
CMD [ "poetry", "run", "python", "app"]