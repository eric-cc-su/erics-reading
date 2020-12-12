#!/bin/bash

ENDPOINT=""

if [ -z "$1" ]; then
    # No filepath argument given
    if [ ! -f "config.ini" ]; then
        echo "Required configuration file not found"
    else
        ENDPOINT=$(python3 compile_gr_endpoint.py config.ini)
    fi
elif [ ! -f "$1" ]; then
    # Argument given does not represent valid filepath
    echo "$1 is not a valid file"
else
    echo "Using $1"
    ENDPOINT=$(python3 compile_gr_endpoint.py $1)
fi

# Save data to temporary XML file and process XML
XML_FILEPATH="tmp_gr_shelf.xml"
if [ ! -z ENDPOINT ]; then
    curl $ENDPOINT > $XML_FILEPATH
    python3 parse_currently_reading.py $XML_FILEPATH
fi

# Remove temporary XML file
if [ -f $XML_FILEPATH ]; then
    rm $XML_FILEPATH
fi