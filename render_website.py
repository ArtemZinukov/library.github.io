import json
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

pages_dir = "pages"


def create_pages_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def load_books():
    with open("media/books/books_info.json", "r", encoding='utf-8') as file:
        books_json = file.read()
    books = json.loads(books_json)
    return books


def chunk_books(books, books_per_page):
    return list(chunked(books, books_per_page))


def render_page(page_books, page_num, total_pages):

    template = env.get_template('template.html')
    rendered_page = template.render(books=page_books,
                                    page_num=page_num,
                                    total_pages=total_pages)

    file_path = os.path.join(pages_dir, f'index{page_num}.html')
    with open(file_path, 'w', encoding="utf8") as file:
        file.write(rendered_page)


def on_reload():
    books = load_books()
    chunked_books = chunk_books(books, 20)
    total_pages = len(chunked_books)

    for page_num, page_books in enumerate(chunked_books, start=1):
        render_page(page_books, page_num, total_pages)


def main():
    create_pages_directory(pages_dir)
    on_reload()

    server = Server()
    server.watch('media/books/books_info.json', on_reload)
    server.watch('media/books/*.txt', on_reload)
    server.watch('media/books/*.jpg', on_reload)
    server.watch('template.html', on_reload)
    server.watch('pages/*.html', on_reload)

    server.serve(root='.')


if __name__ == "__main__":
    main()
