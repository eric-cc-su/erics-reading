import os
import re
import sys
import xml.etree.ElementTree as ET

from typing import Any, Dict

def generate_books_html(book_dict: Dict[str, Any]):
    """
    Assemble HTML entries for all books given in book_dict.
    """
    template = ""
    with open("templates/book-container-template.html", "r") as template_file:
        template = template_file.read()

    for book in book_dict:
        title_split = book.get("title").split(":")
        book_title = title_split[0]
        subtitle = "" if len(title_split) == 1 else title_split[1].strip()
        if len(title_split) > 2:
            subtitle = ":".join(title_split[1:])

        # Update Image URL with core URL
        image_url = book.get("image_url")
        # Image URL regex: (\/<BOOK-ID>\.)([A-Za-z0-9_]+\.)?(jpg|jpeg|png)
        image_url_regex = re.compile('(\/<BOOK-ID>\.)([A-Za-z0-9_]+\.)?(jpg|jpeg|png)'.replace("<BOOK-ID>", str(book.get("id"))))
        match = image_url_regex.search(image_url)
        if match:
            image_url = image_url_regex.sub("{}{}".format(match.group(1), match.group(3)), image_url)

        # Update HTML template
        book_template = template.replace(
            "book_url", book.get("url")
        ).replace(
            "image_url", image_url
        ).replace(
            "alt=\"book cover image\"", "alt=\"{} cover image\"".format(book_title)
        ).replace(
            "<h2 class=\"book-title\">Title</h2>", "<h2 class=\"book-title\">{}</h2>".format(book_title)
        )

        if subtitle:
            book_template = book_template.replace("<h3 class=\"book-subtitle\">Subtitle Text</h3>", "<h3 class=\"book-subtitle\">{}</h3>".format(subtitle))
        else:
            book_template = book_template.replace("<h3 class=\"book-subtitle\">Subtitle Text</h3>\n", "")
        print(book_template)


def parse_xml(filepath: str) -> Dict[str, Any]:
    """
    Parse given XML file to find books in currently reading shelf.

    Structure of shelf is expected to be:
    <shelf name=""></shelf>
    <reviews start="" end="" total="">
        <review>
            <book>
                <id type=""></id>
                <title>
                <title_without_series>
                <image_url>
                <link>
            </book>
        </review>
    </reviews>
    """
    gr_tree = ET.parse(filepath)
    shelves = gr_tree.findall('shelf')
    books = []

    if len(shelves) != 1:
        print("Expected one shelf. Found %d. Exiting" % len(shelves))
    elif shelves[0].get("name") != "currently-reading":
        print("Shelf has name %s. Expected name %s. Exiting" % (shelves[0].get("name"), "currently-reading"))
    else:
        # Iterate over books in shelf
        for book in gr_tree.findall('reviews/review/book'):
            book_id = book.find("id")
            # TODO: Fetch and assemble author names
            book_item = {
                "id": book_id.text if book_id.get("type") != "integer" else int(book_id.text),
                "title": book.find("title_without_series", book.find("title")).text,
                "image_url": book.find("image_url").text,
                "url": book.find("link").text
            }
            books.append(book_item)

    return books

if __name__=="__main__":
    filename = "parse_shelf"
    if len(sys.argv) < 2:
        print("%s requires XML filepath as first parameter" % (filename))
    else:
        filepath = sys.argv[1]
        if os.path.isfile(filepath):
            print("Parsing file: %s" % filepath)
            generate_books_html(parse_xml(filepath))
        else:
            print("%s is not a valid file" % filepath)