#!/bin/bash

# Check if result.11 exists
if [ ! -f result.ll ]; then
    echo "result.ll not found!"
    exit 1
fi

# Step 1: Compile LLVM IR to assembly
llc result.ll
if [ $? -ne 0 ]; then
    echo "Error: llc result failed!"
    exit 1
fi

# Step 2: Compile assembly to object file
gcc -c result.s
if [ $? -ne 0 ]; then
    echo "Error: gcc result of result.s failed!"
    exit 1
fi

# Step 3: Compile aux_functions.c to object file
gcc -c aux_functions.c -lm
if [ $? -ne 0 ]; then
    echo "Error: gcc result of aux_functions.c failed!"
    exit 1
fi

# Step 4: Link the object files and create the executable
gcc result.o aux_functions.o -o a.out -lm
if [ $? -ne 0 ]; then
    echo "Error: linking failed!"
    exit 1
fi

# Step 5: Run the executable
./a.out