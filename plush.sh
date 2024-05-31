#!/bin/bash

# Function to display usage information
usage() {
    echo "Usage: plush [--tree] filename.pl"
    exit 1
}

# Check if there are no arguments
if [ $# -eq 0 ]; then
    usage
fi

# Initialize variables
TREE_FLAG=false
FILENAME=""

# Parse the arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --tree) TREE_FLAG=true ;;
        *.pl) FILENAME="$1" ;;
        *) echo "Unknown parameter: $1" ; usage ;;
    esac
    shift
done

# Check if the filename is provided
if [ -z "$FILENAME" ]; then
    echo "Error: No filename provided."
    usage
fi

# Call the compiler
if $TREE_FLAG; then
    python3 main.py --tree "$FILENAME"
else
    python3 main.py "$FILENAME"
fi