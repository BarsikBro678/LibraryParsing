import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import math

from more_itertools import chunked
from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape

try:
    os.makedirs("pages/")
except:
    pass


def reload():
    with open("books.json", "r", encoding="utf8") as file:
        books_json = file.read()
    books = json.loads(books_json)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    books_pages = list(chunked(books, 20))
    for page_num, books_page in enumerate(books_pages):
        rendered_page = template.render(
            books=list(chunked(books_page, 2)),
            pages_all=len(books_pages)+1,
            current_page=page_num+1,
        )
        with open(f'pages/index{page_num+1}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


server = Server()
server.watch('template.html', reload)
server.serve(root='.', default_filename="pages/index1.html")