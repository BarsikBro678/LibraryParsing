import os
import argparse
import time

from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
import requests
from urllib.parse import urljoin, urlparse


def check_for_redirect(response):
    history = response.history
    if history:
        raise requests.HTTPError


def download_txt(response, filename, folder='books/'):
    os.makedirs(folder, exist_ok=True)
    filename = sanitize_filename(filename)
    filename = filename.strip()
    path = os.path.join(folder, f"{filename}.txt")
    with open(path, "wb") as file:
        file.write(response.content)


def download_image(url, filename, folder="images/"):
    os.makedirs(folder, exist_ok=True)
    filename = sanitize_filename(filename)
    filename = filename.strip()
    response = requests.get(url)
    response.raise_for_status()
    path = os.path.join(folder, f"{filename}")
    with open(path, "wb") as file:
        file.write(response.content)


def parse_book_page(book_response, book_url):
    soup = BeautifulSoup(book_response.text, 'lxml')

    title_tag = soup.find("h1")
    title, author = title_tag.text.split(" :: ")

    image_tag = soup.select_one("div.bookimage img")
    image_url = urljoin(book_url, image_tag["src"])
    image_parse = urlparse(image_url)
    image_path = image_parse.path.split("/")[-1]
    comments_tag = soup.select("div.texts")
    genres_tag = soup.select_one("span.d_book")
    genres_tag = genres_tag.select("a")

    book = {
        "title": title.replace("\xa0", ""),
        "author": author.replace("\xa0", ""),
        "comments": list(map(lambda x: x.text.replace("\xa0", ""), comments_tag)),
        "genres": list(map(lambda x: x.text.replace("\xa0", ""), genres_tag)),
        "image_url": image_url.replace("\xa0", ""),
        "image_path": image_path.replace("\xa0", ""),
        "image_src": image_tag["src"].replace("\xa0", ""),
    }
    return book


def main():
    parser = argparse.ArgumentParser(
        description="Эта программа скачивает книги с сайта tululu.org",
    )
    parser.add_argument("--start_id", default=1, type=int, help="id начиная с которого скачиваются книги. Стандртное значение - 1.")
    parser.add_argument("--end_id", default=11, type=int, help="id после которого книги не скачиваются. Стандартное значение - 11.")

    args = parser.parse_args()
    start_id = args.start_id
    end_id = args.end_id

    for book_id in range(start_id, end_id):
        payload = {
            'id': book_id,
        }
        try:
            response = requests.get('https://tululu.org/txt.php', params=payload)
            response.raise_for_status()
            check_for_redirect(response)

            book_url = f'https://tululu.org/b{book_id}/'
            book_response = requests.get(book_url)
            book_response.raise_for_status()
            check_for_redirect(book_response)

            book = parse_book_page(book_response, book_url)
            filename = f"{book_id}.{book['title']}"
            download_txt(response, filename)
            download_image(book["image_url"], book["image_path"])
        except requests.HTTPError:
            print(f"На сайте нет книги с id = {book_id}")
        except requests.ConnectionError:
            print("Ошибка подключения")
            time.sleep(10)


if __name__ == '__main__':
    main()