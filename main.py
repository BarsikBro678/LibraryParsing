import argparse
import os
import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlparse

def check_for_redirect(response):
    history = response.history
    if history != []:
        raise requests.HTTPError


def download_txt(response, filename, folder='books/'):
    os.makedirs(folder, exist_ok=True)
    filename = sanitize_filename(filename)
    filename = filename.strip()
    path = os.path.join(folder, f"{filename}.txt")
    with open(path, "wb") as file:
        file.write(response.content)


def download_image(response, filename, folder="images/"):
    os.makedirs(folder, exist_ok=True)
    filename = sanitize_filename(filename)
    filename = filename.strip()
    path = os.path.join(folder, f"{filename}.jpg")
    with open(path, "wb") as file:
        file.write(response.content)


def parse_book_page(book_response, id):
    soup = BeautifulSoup(book_response.text, 'lxml')

    title_tag = soup.find('h1')
    title, author = title_tag.text.split(" :: ")
    filename = f"{id}.{title}"

    image_tag = soup.find('div', class_="bookimage")
    image_tag = image_tag.find('img')
    image_url = urljoin("https://tululu.org/", image_tag["src"])
    image_parse = urlparse(image_url)
    image_response = requests.get(image_url)
    image_response.raise_for_status()
    image_path = image_parse.path.replace("/images", "").replace(".gif", "").replace("/shots", "").replace(".jpg", "")

    comments_tag = soup.find_all('div', class_="texts")
    genres_tag = soup.find('span', class_="d_book")
    genres_tag = genres_tag.find_all("a")

    book_data = {
        "title": title,
        "author": author,
        "comments": list(map(lambda x: x.text, comments_tag)),
        "genres": list(map(lambda x: x.text, genres_tag)),
        "image_response": image_response,
        "image_path": image_path,
        "filename": filename,
    }
    return book_data




def main():
    parser = argparse.ArgumentParser(
        description="Эта программа скачивает книги с сайта tululu.org",
    )
    parser.add_argument("--start_id", default=1, type=int, help="id начиная с которого скачиваются книги. Стандртное значение - 1.")
    parser.add_argument("--end_id", default=10, type=int, help="id после которого книги не скачиваются. Стандартное значение - 10.")

    args = parser.parse_args()
    start_id = int(args.start_id)
    end_id = int(args.end_id)
    for id in range(start_id, end_id+1):
        payload = {
            'id': id,
        }
        try:
            response = requests.get('https://tululu.org/txt.php', params=payload)
            response.raise_for_status()
            check_for_redirect(response)

            book_url = f'https://tululu.org/b{id}/'
            book_response = requests.get(book_url)
            book_response.raise_for_status()

            book_data = parse_book_page(book_response, id)
            print(book_data)
            download_txt(response, book_data["filename"])
            download_image(book_data["image_response"], book_data["image_path"])
        except requests.HTTPError:
            pass

if __name__ == '__main__':
    main()