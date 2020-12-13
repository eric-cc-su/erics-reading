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
INDEX_FILEPATH="src/index.html"
HTML_FILEPATH=""

if [ ! -z $ENDPOINT ]; then
    curl $ENDPOINT > $XML_FILEPATH
    HTML_FILEPATH=$(python3 parse_currently_reading.py $XML_FILEPATH)
    if [ $? -eq 0 ]; then
        open -a "Google Chrome" $HTML_FILEPATH

        # https://www.shellhacks.com/yes-no-bash-script-prompt-confirmation/
        while true; do
            read -p "Overwrite current index.html with auto-generated HTML? (y/n)" yn
            case $yn in
                [Yy]* )
                    rm $INDEX_FILEPATH
                    mv $HTML_FILEPATH $INDEX_FILEPATH
                    break;;
                [Nn]* )
                    rm $HTML_FILEPATH
                    break;;
                * ) echo "Please answer yes or no.";;
            esac
        done
    fi
fi

# Remove temporary XML file
if [ -f $XML_FILEPATH ]; then
    rm $XML_FILEPATH
fi