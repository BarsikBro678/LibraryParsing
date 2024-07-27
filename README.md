# Парсер книг о фантастике с сайта tululu.org 

Этот проект скачивает книги с [tululu.org](https://tululu.org).

Не 1, не 2.....

Сколько угодно книг, какие угодно книги, и всю инофрмация об этих книгах.

### Как установить

В проекте используется python 3.x.

Перед запуском кода нужно написать в командную строку:

```pip install -r requirements.txt ```

Запустить код:

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

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).