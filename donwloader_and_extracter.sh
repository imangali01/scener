#!/bin/bash

# Download the tar files
for n in {0..19}
do
    wget https://github.com/imangali01/scener-dataset/releases/download/v1.0/scener_${n}.tar
done

# Extract the tar files
for n in {0..19}
do
    tar -zxf scener_${n}.tar
done
