#! /bin/bash

# Creating poetry venv
cd /app && poetry install

# Inputs arguments
pr_number=$1
draft=$2
prerelease=$3
generate_release_notes=$4

# Build the command based on available parameters
CMD="poetry run python3 /app/create_new_release.py --pr_number \"$pr_number\""


if [ -n "$draft" ]; then
    CMD="$CMD --draft \"$draft\""
fi

if [ -n "$prerelease" ]; then
    CMD="$CMD --prerelease \"$prerelease\""
fi

if [ -n "$generate_release_notes" ]; then
    CMD="$CMD --generate_release_notese \"$generate_release_notes\""
fi

# Print and execute the command
echo "Executing command: $CMD"
eval "$CMD"