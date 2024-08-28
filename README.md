# Парсер книг о фантастике с сайта tululu.org 

Этот проект скачивает книги с [tululu.org](https://tululu.org).

## Как установить

В проекте используется python 3.x.

Перед запуском кода нужно написать в командную строку:

```pip install -r requirements.txt ```

## Книги с главной страницы

Заупстить:

```python download_all_books.py```

### Аргемнты

При запуске проекта имеются следующие аргументы:

`start_id`: id начиная с которого скачиваются книги. Стандртное значение - 1.

```python download_all_books.py --start_id 10```

`end_id`: id после которого книги не скачиваются. Стандартное значение - 11.

```python download_all_books.py --end_id 2```

## Книги о научной фантастике

Запустить:

```python parse_tululu_category.py```

### Аргументы


При запуске проекта имеются следуйщие параметры:

`--start_page`: Страница начиная с которой скачиваются книги. Стандртное значение - 1.

```python parse_tululu_category.py --start_page 3```

`--end_page`: Страница начиная с которой книги не скачиваются. Стандартное значение - 11.

```python parse_tululu_category.py --end_page 5```

`--dest_folder`: Путь к каталогу с результатами парсинга: картинкам, книгам, JSON.

```python parse_tululu_category.py --dest_folder result/```

`--skip_img`: Не скачивать картинки. 

```python parse_tululu_category.py --skip_img```

`--skip_txt`: Не скачивать книги.

```python parse_tululu_category.py --skip_txt```

# Сайт с книгами

В файле `render_website.py` можно запустить сайт по каманде в терминале:
```
python render_website.py
```

Адрес сайта -  [http://127.0.0.1:5500/pages/index1.html](http://127.0.0.1:5500/pages/index1.html)


## Github Pages

Ссылка на проект - [https://barsikbro678.github.io/LibraryParsing/](https://barsikbro678.github.io/LibraryParsing/).

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).