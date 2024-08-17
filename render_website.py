import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

from livereload import Server, shell
from jinja2 import Environment, FileSystemLoader, select_autoescape

def reload():
    with open("books.json", "r", encoding="utf8") as file:
        books_json = file.read()
    books = json.loads(books_json)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        books=books,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


server = Server()
server.watch('template.html', reload)
server.serve(root='index.html')
