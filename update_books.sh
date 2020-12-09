#!/bin/bash
if [ -z "$1" ]; then
    if [ ! -f "config.ini" ]; then
        echo "Required configuration file not found"
    fi
elif [ ! -f "$1" ]; then
    echo "$1 is not a valid file"
else
    echo "Using $1"
fi
