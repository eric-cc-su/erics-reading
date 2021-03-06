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
    html = ""
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
        image_url_regex = re.compile("(\/<BOOK-ID>\.)([A-Za-z0-9_]+\.)?(jpg|jpeg|png)".replace("<BOOK-ID>", str(book.get("id"))))
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
        ).replace(
            "<h4 class=\"book-author\">Author</h4>", "<h4 class=\"book-author\">{}</h4>".format(book.get("author"))
        )

        if subtitle:
            book_template = book_template.replace("<h3 class=\"book-subtitle\">Subtitle Text</h3>", "<h3 class=\"book-subtitle\">{}</h3>".format(subtitle))
        else:
            book_template = book_template.replace("<h3 class=\"book-subtitle\">Subtitle Text</h3>\n", "")
        html += book_template

    return html

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
        for book in gr_tree.findall("reviews/review/book"):
            book_id = book.find("id")
            authors = ", ".join(map(lambda author: author.find("name").text, book.findall("authors/author")))

            book_item = {
                "id": book_id.text if book_id.get("type") != "integer" else int(book_id.text),
                "title": book.find("title_without_series", book.find("title")).text,
                "author": authors,
                "image_url": book.find("image_url").text,
                "url": book.find("link").text
            }
            books.append(book_item)

    return books

def update_index(book_dict: Dict[str, Any], new_index_filepath: str="src/index_autogenerated.html") -> str:
    """
    Given new HTML for the books carousel, updates the index.html file.

    Returns the filepath of the new index file.
    """
    index_html = ""
    with open("templates/index.html", "r") as index_template:
        index_html = index_template.read()

    if len(book_dict) == 0:
        index_html = index_html.replace(
            "<h1 class=\"site-title-header\">Eric's Reading:</h1>",
            "<h1 class=\"site-title-header\">Eric's taking a break</h1>"
        ).replace(
        "<div id=\"books-carousel\"><!-- BOOK HTML HERE --></div>",
        "",
        )
    else:
        index_html = index_html.replace(
            "<div id=\"books-carousel\"><!-- BOOK HTML HERE --></div>",
            "<div id=\"books-carousel\">\n{}\n</div>".format(generate_books_html(book_dict))
        )

    with open(new_index_filepath, "w") as new_index_file:
        new_index_file.write(index_html)

    return new_index_filepath

if __name__=="__main__":
    filename = "parse_shelf"
    if len(sys.argv) < 2:
        print("%s requires XML filepath as first parameter" % (filename))
        sys.exit(1)
    else:
        filepath = sys.argv[1]
        if os.path.isfile(filepath):
            print(update_index(parse_xml(filepath)))
            sys.exit(0)
        else:
            print("%s is not a valid file" % filepath)
            sys.exit(1)
