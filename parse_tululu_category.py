import os
import argparse
import json
from urllib.parse import urljoin
import time

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

from download_all_books import download_txt, download_image, parse_book_page, check_for_redirect


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
    for page_num in range(start_page, end_page):
        try:
            url = f"https://tululu.org/l55/{page_num}"
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)
            soup = BeautifulSoup(response.text, "lxml")
            books = soup.select(".d_book")
            for book_num, book_tag in enumerate(books):
                try:
                    book_tag = book_tag.select_one("a")
                    book_url_part = book_tag["href"]
                    book_url = urljoin(url, book_url_part)
                    book_response = requests.get(book_url)
                    book_response.raise_for_status()
                    check_for_redirect(book_response)
                    book = parse_book_page(book_response, book_url)
                    book_id = book_url_part[2:-1]
                    filename = f"{book_id}.{book['title']}"
                    if not skip_txt:
                        download_txt(book_response, filename, folder = f"{dest_folder}books/")
                    if not skip_imgs:
                        download_image(book["image_url"], book["image_path"], folder = f"{dest_folder}images/")
                    book_args = {"title": book["title"],
                                 "author": book["author"],
                                 "img_src": book["image_src"],
                                 "book_path": filename,
                                 "comments": book["comments"],
                                 "genres": book["genres"],
                    }
                    books_args.append(book_args)
                except requests.exceptions.HTTPError:
                    print(f"Книга №{book_num} со страницы {page_num} не скачана")
                except requests.exceptions.ConnectionError:
                    print("Ошибка соеденения")
                    time.sleep(10)
        except requests.exceptions.HTTPError:
            print(f"Страница {page_num} не скачана")
        except requests.exceptions.ConnectionError:
            print("Ошибка подключения")
            time.sleep(10)
    with open(f"{dest_folder}books.json", "w", encoding="utf8") as file:
        json.dump(books_args, file, ensure_ascii=False)


if __name__ == "__main__":
    main()