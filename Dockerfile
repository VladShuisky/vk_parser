FROM python:3.10-slim

RUN pip install --upgrade pip
RUN pip install poetry

# Copy only requirements to cache them in docker layer
WORKDIR /app
COPY poetry.lock pyproject.toml /app/

# Project initialization:
RUN #poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --no-root

# Creating folders, and files for a project:
# COPY . /app
