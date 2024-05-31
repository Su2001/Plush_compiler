#!/bin/bash

docker build -t plush .

echo "Setup complete. You can now use the plush."

if [["$OSTYPE" == "msys" | "$OSTYPE" == "win32"]]; then
    winpty docker run -it plush:latest sh
else
    docker run -it plush:latest sh
fi