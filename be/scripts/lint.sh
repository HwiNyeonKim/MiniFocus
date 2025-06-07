#!/bin/bash

# Change to the project root directory
cd "$(dirname "$0")/.." || exit

# Run isort
echo "Running isort..."
poetry run isort .

# Run black
echo "Running black..."
poetry run black .

# Run flake8
echo "Running flake8..."
poetry run flake8 .