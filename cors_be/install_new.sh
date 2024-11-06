#!/bin/bash

# Check if module name is provided
if [ -z "$1" ]; then
  echo "Usage: $0 <module_name>"
  exit 1
fi

MODULE_NAME=$1

# Install the module using pip
pip install "$MODULE_NAME"

# Check if the module was installed successfully
if [ $? -ne 0 ]; then
  echo "Failed to install $MODULE_NAME"
  exit 1
fi

# Update requirements.txt with the current list of installed packages
pip freeze > requirements.txt

echo "$MODULE_NAME has been installed and added to requirements.txt"