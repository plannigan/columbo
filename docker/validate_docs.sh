#!/usr/bin/env bash
# this script will exit if one of the example files does not execute properly with python

# this is set so that the script fails if one example fails to be executed properly
set -e

for filename in docs/examples/*.py; do
    printf "\n\n --- %s ---\n" "${filename}"
    # provide default answers if example python file asks for input
    yes "" | python "${filename}";
done

# this will only get printed if all examples finish successfully
printf "\n\n\nAll of the documentation examples can be run!";
