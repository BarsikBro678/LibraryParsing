import json
import os

from more_itertools import chunked
from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape


BOOKS_IN_PAGE = 20


def reload():
    with open(f"books.json", "r", encoding="utf8") as file:
        books = json.load(file)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    pages_with_books = list(chunked(books, BOOKS_IN_PAGE))

    for page_num, books_page in enumerate(pages_with_books, start=1):
        rendered_page = template.render(
            books=list(chunked(books_page, 2)),
            pages_all=len(pages_with_books)+1,
            current_page=page_num,
        )
        with open(f'pages/index{page_num}.html', 'w', encoding="utf8") as file:
            file.write(rendered_page)


def main():
    reload()
    os.makedirs("pages/", exist_ok=True)
    server = Server()
    server.watch('template.html', reload)
    server.serve(root='.', default_filename="pages/index1.html")


if __name__ == "__main__":
    main()