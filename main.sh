#!/bin/bash

VENV_NAME=".venv"

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

echo "Checking for \`python3\` package..."
if ! command_exists python3; then
    echo "Python 3 is not found. Please ensure Python 3 is installed and added to your PATH."
    exit 1
fi

echo "Looking for venv..."
if [ ! -d "$VENV_NAME" ]; then
    echo "Creating new virtual environment: $VENV_NAME"
    python3 -m venv "$VENV_NAME"
    if [ $? -ne 0 ]; then
        echo "Failed to create virtual environment. Please check your Python installation."
        exit 1
    fi
else
    echo "Virtual environment $VENV_NAME already exists."
fi

echo "Activating venv..."
source "$VENV_NAME/bin/activate"

echo "Checking for requirements.txt"
if [ ! -f "requirements.txt" ]; then
    echo "requirements.txt not found. Please create a requirements.txt file in the same directory as this script."
    exit 1
fi

echo "Upgrading pip..."
python3 -m pip install --upgrade pip

echo "Installing packages from requirements.txt..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install some packages. Please check your internet connection and requirements.txt file."
    exit 1
fi

echo "Launching script..."
python3 main.py "$@"

echo "Deactivating venv..."
deactivate

echo "All done"
