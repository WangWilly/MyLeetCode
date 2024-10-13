#/bin/bash

# Target directory
if [ -z "$1" ]; then
    echo "Please provide the target directory"
    exit 1
fi

TargetDir=$1

# Build
echo "\nResetting and building..."
cd $TargetDir
make clean

# check `tree` is installed
if [ -x "$(command -v tree)" ]; then
    tree .
fi
make

# Run
echo "\nRunning..."
./solution
