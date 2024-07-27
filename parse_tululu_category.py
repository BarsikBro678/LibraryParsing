import os
import argparse
import json

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

from main import download_txt, download_image, parse_book_page

def write_books_args(books_args, filename="books_args"):
    filename = sanitize_filename(filename)
    filename = filename.strip()
    with open(f"{filename}.json", "w", encoding="utf8") as file:
        json.dump(books_args, file, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description="Эта программа скачивает книги о фантастике с сайта tululu.org",
    )
    parser.add_argument("--start_page", default=1, type=int,
                        help="Страница начиная с которой скачиваются книги о фантастике. Стандартное значение - 1.")
    parser.add_argument("--end_page", default=10, type=int,
                        help="Страница на которой книги уже не скачиваются. Стандартное значение - 10.")

    args = parser.parse_args()
    start_page = args.start_page
    end_page = args.end_page
    books_args = []
    for page in range(start_page, end_page):
        url = f"https://tululu.org/l55/{page}"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        books = soup.select(".d_book")
        for num in range(len(books)):
            book_tag = books[num].select_one("a")
            book_id = book_tag["href"]
            book_url = f'https://tululu.org/{book_id}'
            book_response = requests.get(book_url)
            book_response.raise_for_status()
            book = parse_book_page(book_response, book_id[2:])
            download_txt(response, book["filename"])
            download_image(book["image_url"], book["image_path"])
            book_args = {"title": book["title"].replace("\xa0", ""),
                         "author": book["author"].replace("\xa0", ""),
                         "img_src": book["image_src"].replace("\xa0", ""),
                         "book_path": book["filename"].replace("\xa0", ""),
                         "comments": list(map(lambda x: x.replace("\xa0", ""), book["comments"])),
                         "genres": list(map(lambda x: x.replace("\xa0", ""), book["genres"])),
            }
            books_args.append(book_args)
    write_books_args(books_args)

if __name__ == "__main__":
    main()