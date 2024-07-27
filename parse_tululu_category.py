import os
import argparse
import json

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

from main import download_txt, download_image, parse_book_page


def write_books_args(books_args, filename="books_args", folder=""):
    filename = sanitize_filename(filename)
    filename = filename.strip()
    with open(f"{folder}{filename}.json", "w", encoding="utf8") as file:
        json.dump(books_args, file, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description="Эта программа скачивает книги о фантастике с сайта tululu.org",
    )
    parser.add_argument("--start_page", default=1, type=int,
                        help="Страница начиная с которой скачиваются книги о фантастике. Стандартное значение - 1.")
    parser.add_argument("--end_page", default=11, type=int,
                        help="Страница на которой книги уже не скачиваются. Стандартное значение - 11.")
    parser.add_argument("--dest_folder", default="", type=str,
                        help="Путь к каталогу с результатами парсинга: картинкам, книгам, JSON.")
    parser.add_argument("--skip_imgs", action="store_true",
                        help="Не скачивать картинки.")
    parser.add_argument("--skip_txt", action="store_true",
                        help="Не скачивать книги.")
    args = parser.parse_args()
    start_page = args.start_page
    end_page = args.end_page
    dest_folder = args.dest_folder
    skip_imgs = args.skip_imgs
    skip_txt = args.skip_txt
    books_args = []
    if dest_folder != "":
        os.makedirs(dest_folder)
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
            if not skip_txt:
                download_txt(response, book["filename"], folder = f"{dest_folder}books/")
            if not skip_imgs:
                download_image(book["image_url"], book["image_path"], folder = f"{dest_folder}images/")
            book_args = {"title": book["title"].replace("\xa0", ""),
                         "author": book["author"].replace("\xa0", ""),
                         "img_src": book["image_src"].replace("\xa0", ""),
                         "book_path": book["filename"].replace("\xa0", ""),
                         "comments": list(map(lambda x: x.replace("\xa0", ""), book["comments"])),
                         "genres": list(map(lambda x: x.replace("\xa0", ""), book["genres"])),
            }
            books_args.append(book_args)
    write_books_args(books_args, folder = dest_folder)


if __name__ == "__main__":
    main()