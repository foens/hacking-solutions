#!/bin/bash

# sudo apt-get update
# sudo apt-get install gcc-arm-linux-gnueabihf binutils-arm-linux-gnueabihf

mkdir -p out
arm-linux-gnueabihf-gcc -march=armv7 -s solution.c -o out/solution
cat out/solution | base64 > out/solution.base64
