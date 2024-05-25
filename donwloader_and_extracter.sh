#!/bin/bash

# Default value
num_files=19

# Parse command-line argument
while getopts "f:" opt; do
  case $opt in
    f) num_files=$OPTARG ;;
    \?) echo "Invalid option -$OPTARG" >&2 ;;
  esac
done

echo '[+] STARTING DOWNLOADING!'

# Download the tar files
for n in $(seq 0 $num_files)
do
    echo '[+] DOWNLOADING scener_'$n'.tar...'
    wget https://github.com/imangali01/scener-dataset/releases/download/v1.0/scener_${n}.tar
done

echo '[+] COMPLETED DOWNLOADING!'
echo '[+] STARTING UNPACKING!'

# Extract the tar files
for n in $(seq 0 $num_files)
do
    echo '[+] UNPACKING scener_'$n'.tar...'
    tar -zxf scener_${n}.tar
done

echo '[+] COMPLETED!'
