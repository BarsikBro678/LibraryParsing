import os

import requests
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename

from main import download_txt, download_image, parse_book_page

def main():
    max_page = 4
    for page in range(1, max_page+1):
        url = f"https://tululu.org/l55/{page}"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        books = soup.find_all(class_="d_book")
        for num in range(len(books)):
            book_tag = books[num].find("a")
            book_id = book_tag["href"]
            book_url = f'https://tululu.org/{book_id}'
            book_response = requests.get(book_url)
            book_response.raise_for_status()
            book = parse_book_page(book_response, book_id[2:])
            download_txt(response, book["filename"])
            download_image(book["image_url"], book["image_path"])



if __name__ == "__main__":
    main()