#! /bin/bash

# Creating poetry venv
cd /app && poetry install

# Build the command based on available parameters
CMD="poetry run python3 /app/create_new_release.py"

# Print and execute the command
echo "Executing command: $CMD"
eval "$CMD"