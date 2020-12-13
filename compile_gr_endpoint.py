import configparser
import os
import sys

def compile_endpoint(configuration_filepath: str) -> str:
    """
    Use configuration filepath to compile API endpoint for currently reading shelf from Goodreads.
    """
    parser = configparser.ConfigParser()
    parser.read(configuration_filepath)

    gr_user_id = parser.get("Goodreads", "user_id")
    gr_key = parser.get("Goodreads", "key")
    # API endpoint
    endpoint = "https://www.goodreads.com/review/list/<USER-ID>.xml?key=<KEY>&v=2&shelf=currently-reading".replace("<USER-ID>", gr_user_id).replace("<KEY>", gr_key)

    return endpoint

if __name__ == "__main__":
    # sys.argv[0] is script itself
    if len(sys.argv) < 2:
        print("Script requires configuration filepath as first parameter")
    elif not os.path.isfile(sys.argv[1]):
        # Ensure first argument is valid filepath
        print("%s is not a valid file" % sys.argv[1])
    else:
        print(compile_endpoint(sys.argv[1]))
