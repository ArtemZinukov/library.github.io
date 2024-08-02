import json
import argparse
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked

PAGES_DIR = 'pages'


def load_books(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        books = json.load(file)
    return books


def render_page(page_books, page_num, total_pages, env):
    template = env.get_template('template.html')
    rendered_page = template.render(books=page_books,
                                    page_num=page_num,
                                    total_pages=total_pages)
    file_path = os.path.join(PAGES_DIR, f'index{page_num}.html')
    with open(file_path, 'w', encoding='utf8') as file:
        file.write(rendered_page)


def on_reload(dest_folder, env):
    books = load_books(dest_folder)
    books_per_page = 20
    chunked_books = list(chunked(books, books_per_page))
    total_pages = len(chunked_books)

    for page_num, page_books in enumerate(chunked_books, start=1):
        render_page(page_books, page_num, total_pages, env)


def create_parser():
    parser = argparse.ArgumentParser(prog='render_website',
                                     description='запускает скрипт для создания сайта с книгами')
    parser.add_argument('--dest_folder', help='Укажите путь, где хранится файл json',
                        type=str, default='./media/books_info.json')
    return parser


def main():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    parser = create_parser()
    parser_args = parser.parse_args()

    os.makedirs(PAGES_DIR, exist_ok=True)

    on_reload(parser_args.dest_folder, env)

    server = Server()
    server.watch('template.html', lambda: on_reload(parser_args.dest_folder, env))

    server.serve(root='.', default_filename='pages/index1.html')


if __name__ == '__main__':
    main()
