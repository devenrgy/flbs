import os
import sys

import cache
import db
import downloader
from config import PAGE_SIZE
from db import BookRow
from fmt import (
    apply_lang,
    apply_sort,
    format_author,
    print_page,
)
from keys import (
    BACK, DOWNLOAD, DOWNLOAD_ALL, FILTER, GOTO, LANG,
    NEXT, OPEN, PREV, QUIT,
    SORT_ASC, SORT_DESC, SORT_RESET,
    hints_list, hints_series,
)
from layout import GAP, terminal_width

_BACK_SIG = "back"


def _clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def _exit() -> None:
    sys.exit(0)


def resolve_by_spec(spec: str, book_cache: list[BookRow]) -> list[BookRow]:
    entries:    list[BookRow] = []
    cache_size: int           = len(book_cache)
    for token in spec.split(","):
        token = token.strip()
        if not token:
            continue
        if token.isdigit() and book_cache and 1 <= int(token) <= cache_size:
            entries.append(book_cache[int(token) - 1])
        else:
            found = [r for r in book_cache if r["FILEID"] == token]
            if found:
                entries.extend(found)
            else:
                row = db.search_by_id(token)
                if row:
                    entries.append(row)
                else:
                    print(f"  Not found: {token!r}")
    return entries


def show_results(
    results:    list[BookRow],
    has_parent: bool = False,
) -> str:
    if not results:
        print("Nothing found.")
        return _BACK_SIG

    original         = results
    sort: str | None = None
    lang: str | None = None
    displayed        = original
    total            = len(displayed)
    page             = 0

    while True:
        total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
        page        = max(0, min(page, total_pages - 1))

        _clear()
        print_page(displayed, page, total, sort, lang, has_parent=has_parent)

        try:
            cmd = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            _exit()

        low = cmd.lower()

        if low in (QUIT.cmd, "quit"):
            _exit()
        elif low == BACK.cmd:
            return _BACK_SIG
        elif low == NEXT.cmd:
            page = min(page + 1, total_pages - 1)
        elif low == PREV.cmd:
            page = max(page - 1, 0)
        elif low == SORT_ASC.cmd:
            sort      = "asc"
            displayed = apply_sort(apply_lang(original, lang), sort)
            total     = len(displayed)
            page      = 0
        elif low == SORT_DESC.cmd:
            sort      = "desc"
            displayed = apply_sort(apply_lang(original, lang), sort)
            total     = len(displayed)
            page      = 0
        elif low == SORT_RESET.cmd:
            sort      = None
            displayed = apply_lang(original, lang)
            total     = len(displayed)
            page      = 0
        elif low.isdigit():
            n = int(low) - 1
            if 0 <= n < total_pages:
                page = n
            else:
                print(f"Page 1–{total_pages}.")
        elif low.startswith(LANG.cmd + " "):
            arg  = low[len(LANG.cmd) + 1:].strip()
            lang = None if arg in ("all", "") else arg
            displayed = apply_sort(apply_lang(original, lang), sort)
            total     = len(displayed)
            page      = 0
            if not displayed:
                print(f"  No books for lang {lang!r} — filter cleared.")
                lang      = None
                displayed = apply_sort(original, sort)
                total     = len(displayed)
        elif low.startswith(DOWNLOAD.cmd + " "):
            spec    = low[len(DOWNLOAD.cmd) + 1:].strip()
            entries = resolve_by_spec(spec, displayed)
            if entries:
                for entry in entries:
                    print(f"\n[{format_author(entry['AUTHOR'])}] {entry['TITLE']}")
                    downloader.extract(entry)
                input("\nPress Enter to continue...")
            else:
                print(f"Not found. Example: {str(DOWNLOAD)}")
        elif low == DOWNLOAD_ALL.cmd:
            if displayed:
                downloader.download_all_books(displayed)
            else:
                print("  No books to download.")
        else:
            pass


def show_series(series_list: list[tuple[str, int]], lang: str | None) -> None:
    if not series_list:
        print("No series found.")
        return

    series_list = sorted(series_list, key=lambda x: x[1], reverse=True)
    tw          = terminal_width() - 1
    sp          = " " * GAP
    page        = 0

    while True:
        total       = len(series_list)
        total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
        page        = max(0, min(page, total_pages - 1))
        start       = page * PAGE_SIZE
        end         = min(start + PAGE_SIZE, total)

        sw  = max((len(series_list[i][0]) for i in range(start, end)), default=40)
        sw  = max(sw, len("SERIES"))
        sw  = min(sw, tw - 4 - GAP * 2 - 6)
        ruler = "─" * (4 + GAP + sw + GAP + 6)

        _clear()
        print(f"{'#':<4}{sp}{'SERIES':<{sw}}{sp}{'BOOKS':>6}")
        print(ruler)
        for i in range(start, end):
            name, cnt = series_list[i]
            name = name if len(name) <= sw else name[:sw - 3] + "..."
            print(f"{i+1:<4}{sp}{name:<{sw}}{sp}{cnt:>6}")
        print(ruler)
        print(f"Page {page+1}/{total_pages}  |  Found: {total} series  |  {hints_series()}")

        try:
            cmd = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            _exit()

        if cmd in (QUIT.cmd, "quit"):
            _exit()
        elif cmd == NEXT.cmd:
            page = min(page + 1, total_pages - 1)
        elif cmd == PREV.cmd:
            page = max(page - 1, 0)
        elif cmd.isdigit():
            n = int(cmd) - 1
            if 0 <= n < total_pages:
                page = n
        elif cmd.startswith(OPEN.cmd + " "):
            token = cmd[len(OPEN.cmd) + 1:].strip()
            if token.isdigit():
                n = int(token) - 1
                if 0 <= n < total:
                    books = db.search_books_in_series(series_list[n][0], lang)
                    if books:
                        cache.save(books)
                        show_results(books, has_parent=True)
                    else:
                        print("No books found in this series.")
                else:
                    print(f"Series 1–{total}.")
            else:
                print(f"Example: {str(OPEN)}")
        elif cmd.startswith(DOWNLOAD.cmd + " "):
            token = cmd[len(DOWNLOAD.cmd) + 1:].strip()
            if token.isdigit():
                n = int(token) - 1
                if 0 <= n < total:
                    books = db.search_books_in_series(series_list[n][0], lang)
                    if books:
                        downloader.download_all_books(books)
                        cache.save(books)
                    else:
                        print("No books found in this series.")
                else:
                    print(f"Series 1–{total}.")
            else:
                print(f"Example: {str(DOWNLOAD)} 1")
        elif cmd.startswith(GOTO.cmd + " "):
            token = cmd[len(GOTO.cmd) + 1:].strip()
            if token.isdigit():
                n = int(token) - 1
                if 0 <= n < total_pages:
                    page = n
                else:
                    print(f"Page 1–{total_pages}.")
            else:
                print(f"Example: {str(GOTO)}")


def show_list(
    rows:        list[tuple[str, int]],
    col_name:    str,
    col_width:   int,
    search_hint: str,
) -> None:
    if not rows:
        print("Nothing found.")
        return

    tw       = terminal_width() - 1
    col_w    = min(col_width, tw - GAP - 6)
    sp       = " " * GAP
    filtered: list[tuple[str, int]] = rows
    query:    str                   = ""
    page:     int                   = 0

    while True:
        total       = len(filtered)
        total_pages = max(1, (total + PAGE_SIZE - 1) // PAGE_SIZE)
        page        = max(0, min(page, total_pages - 1))
        start       = page * PAGE_SIZE
        end         = min(start + PAGE_SIZE, total)
        ruler       = "─" * (col_w + GAP + 6)

        _clear()
        if query:
            print(f"Filter: {query!r}  (/ to reset)")
        print(f"{col_name:<{col_w}}{sp}{'BOOKS':>6}")
        print(ruler)
        for i in range(start, end):
            r    = filtered[i]
            name = r[0] if len(r[0]) <= col_w else r[0][:col_w - 3] + "..."
            print(f"{name:<{col_w}}{sp}{r[1]:>6}")
        print(ruler)
        print(f"Page {page+1}/{total_pages}  |  Total: {total}  |  {hints_list()}")
        print(f"To search: flbs.py {search_hint} <value>")

        try:
            cmd = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            _exit()

        low = cmd.lower()

        if low in (QUIT.cmd, "quit"):
            _exit()
        elif low == NEXT.cmd:
            page = min(page + 1, total_pages - 1)
        elif low == PREV.cmd:
            page = max(page - 1, 0)
        elif low.isdigit():
            n = int(low) - 1
            if 0 <= n < total_pages:
                page = n
        elif cmd.startswith(FILTER.cmd):
            query    = cmd[1:].strip()
            filtered = ([(r[0], r[1]) for r in rows
                         if query.lower() in r[0].lower()]
                        if query else rows)
            page = 0
        else:
            pass
