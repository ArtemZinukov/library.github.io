import json
import argparse
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

pages_dir = 'pages'


def create_pages_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)


def load_books(dest_folder):
    file_path = os.path.join(dest_folder, "books_info.json")
    with open(file_path, 'r', encoding='utf-8') as file:
        books = json.load(file)
    return books


def render_page(page_books, page_num, total_pages):

    template = env.get_template('template.html')
    rendered_page = template.render(books=page_books,
                                    page_num=page_num,
                                    total_pages=total_pages)

    file_path = os.path.join(pages_dir, f'index{page_num}.html')
    with open(file_path, 'w', encoding='utf8') as file:
        file.write(rendered_page)


def on_reload(dest_folder):
    books = load_books(dest_folder)
    books_per_page = 20
    chunked_books = list(chunked(books, books_per_page))
    total_pages = len(chunked_books)

    for page_num, page_books in enumerate(chunked_books, start=1):
        render_page(page_books, page_num, total_pages)


def create_parser():
    parser = argparse.ArgumentParser(prog='render_website',
                                     description='запускает скрипт для создания сайта с книгами')
    parser.add_argument('--dest_folder', help='Укажите путь, где хранится файл json',
                        type=str, default='media/')
    return parser


def main():
    parser = create_parser()
    parser_args = parser.parse_args()

    create_pages_directory(pages_dir)

    on_reload(parser_args.dest_folder)

    server = Server()
    server.watch('media/books_info.json', on_reload)
    server.watch('media/books/*.txt', on_reload)
    server.watch('media/images/*.jpg', on_reload)
    server.watch('template.html', on_reload)
    server.watch('pages/*.html', on_reload)

    server.serve(root='.')


if __name__ == '__main__':
    main()
