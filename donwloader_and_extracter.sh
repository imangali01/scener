#!/bin/bash

echo '[+] STARTING DOWNLOADING!'

# Download the tar files
for n in {0..19}
do
    echo '[+] DOWNLOADING scener_'$n'.tar...'
    wget https://github.com/imangali01/scener-dataset/releases/download/v1.0/scener_${n}.tar
done

echo '[+] COMPLETED DOWNLOADING!'
echo '[+] STARTING UNPACKING!'

# Extract the tar files
for n in {0..19}
do
    echo '[+] UNPACKING scener_'$n'.tar...'
    tar -zxf scener_${n}.tar
done

echo '[+] COMPLETED!'
