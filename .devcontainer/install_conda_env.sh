#!/bin/bash

# Exit if any command fails
set -e

# Define the version of conda and python to use
CONDA_VERSION="4.12.0"
PYTHON_VERSION="3.10"

# Check if conda is already installed
if ! command -v conda &> /dev/null; then
    echo "Conda not found. Installing Miniconda with version $CONDA_VERSION and Python $PYTHON_VERSION..."

    # Download Miniconda installer for Linux with Python 3.10
    wget https://repo.anaconda.com/miniconda/Miniconda3-py310_${CONDA_VERSION}-Linux-x86_64.sh -O Miniconda3.sh

    # Run the installer without manual intervention
    bash Miniconda3.sh -b

    # Initialize conda
    ~/miniconda3/bin/conda init

    # Reload shell to make conda command available
    source ~/.bashrc

    echo "Conda installed successfully."
else
    echo "Conda is already installed. Skipping installation."
fi

# Add conda-forge as the default channel
echo "Adding conda-forge as the default channel..."
conda config --add channels conda-forge
conda config --set channel_priority strict

# Check if environment.yml exists in the current directory
if [[ ! -f "environment.yml" ]]; then
    echo "No environment.yml found in the current directory."
    exit 1
fi

# Create the environment using the environment.yml
echo "Creating environment from environment.yml with Python $PYTHON_VERSION using conda-forge..."
conda env create -f environment.yml --force

echo "Environment created successfully."
