import configparser
import os
import requests
import sys
import xml.etree.ElementTree as xml

def fetch_currently_reading(configuration_filepath):
    """
        Use configuration filepath to fetch currently reading shelf from Goodreads.
    """
    parser = configparser.ConfigParser()
    parser.read(configuration_filepath)

    gr_user_id = parser.get("Goodreads", "user_id")
    gr_key = parser.get("Goodreads", "key")
    # API endpoint
    endpoint = "https://www.goodreads.com/review/list/<USER-ID>.xml?key=<KEY>&v=2&shelf=currently-reading".replace("<USER-ID>", gr_user_id).replace("<KEY>", gr_key)
    gr_response = requests.get(endpoint)

    # et = xml.ElementTree(file=end)
    print(endpoint)

if __name__ == "__main__":
    # sys.argv[0] is script itself
    if len(sys.argv) < 2:
        print("Script requires configuration filepath as first parameter")
    elif not os.path.isfile(sys.argv[1]):
        # Ensure first argument is valid filepath
        print("%s is not a valid file" % sys.argv[1])
    else:
        fetch_currently_reading(sys.argv[1])
