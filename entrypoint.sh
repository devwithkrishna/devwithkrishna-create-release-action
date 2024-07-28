#! /bin/bash

# Creating poetry venv
cd /app && poetry install

# Inputs arguments
token=$1
pr_number=$2
draft=$3
prerelease=$4
generate_release_notes=$5

# Export GH_TOKEN so it can be used by other scripts/commands
export GH_TOKEN="$token"

# Build the command based on available parameters
CMD="poetry run python3 /app/create_new_release.py --pr_number \"$pr_number\""

# Add optional arguments if they are provided
if [ -n "$draft" ]; then
  CMD="$CMD --draft \"$draft\""
fi
if [ -n "$prerelease" ]; then
  CMD="$CMD --prerelease \"$prerelease\""
fi
if [ -n "$generate_release_notes" ]; then
  CMD="$CMD --generate_release_notes \"$generate_release_notes\""
fi

# Print and execute the command
echo "Executing command: $CMD"
eval "$CMD"