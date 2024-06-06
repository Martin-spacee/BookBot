import os
import sys


BOOK_PATH = r'C:\Users\marti\PycharmProjects\BookBot\bookbot\book\Bredberi_Marsianskie-hroniki.txt'
book: dict[int, str] = {}
PAGE_SIZE = 1050


def _get_part_text(text: str, start: int, page_size: int) -> tuple[str, int]:
    signs = [',', '.', '!', ':', ';', '?']
    signs_2 = {'?!': 'XXX', '?..': 'BBB', '!..': 'CCC'}

    for v in signs_2:
        text = text.replace(v, signs_2[v])

    t = text[start:][:page_size]
    if t[-1] not in signs:
        for i in range(len(t) - 1, 0, -1):
            if t[i] in signs:
                t = t[:i + 1]
                break

    for v in signs_2:
        t = t.replace(signs_2[v], v)

    return t, len(t)


def prepare_book(path: str) -> None:
    with open(path, 'r', encoding='utf-8') as file:
        text = file.read()
    start, page_number = 0, 1
    while start < len(text):
        txt, ln = _get_part_text(text, start, PAGE_SIZE)
        book[page_number] = txt.strip()
        start += ln
        page_number += 1


prepare_book(os.path.join(sys.path[0], os.path.normpath(BOOK_PATH)))
