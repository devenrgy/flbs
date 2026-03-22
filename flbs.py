#!/usr/bin/env python3
import os
import sys

import cache
import db
import downloader
import ui


def usage() -> None:
    name = os.path.basename(sys.argv[0])
    print("Usage:")
    print(f"  {name} -a <author>                search by author")
    print(f"  {name} -t <title>                 search by title")
    print(f"  {name} -g <genre>                 search by genre")
    print(f"  {name} -s <series>                show matching series with book counts")
    print(f"  {name} -a <author> -l ru          filter by language")
    print(f"  {name} -a <author> --download 1,3 download #1 and #3")
    print(f"  {name} -e <ID>[,ID2,...]          download directly by ID")
    print(f"  {name} --genres                   list all genres")
    print(f"  {name} --langs                    list all languages")
    print(f"  {name} --reindex                  rebuild index")
    sys.exit(0)


def _parse_args(args: list[str]) -> dict:
    parsed: dict = {
        "flag":       None,
        "query":      None,
        "lang":       None,
        "download":   None,
        "extract_id": None,
    }
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("-a", "-t", "-g", "-s"):
            parsed["flag"] = a
            i += 1
            if i >= len(args):
                usage()
            parsed["query"] = args[i]
        elif a == "-e":
            i += 1
            if i >= len(args):
                usage()
            parsed["extract_id"] = args[i]
        elif a == "-l":
            i += 1
            if i >= len(args):
                usage()
            parsed["lang"] = args[i]
        elif a == "--download":
            i += 1
            if i >= len(args):
                usage()
            parsed["download"] = args[i]
        else:
            usage()
        i += 1
    return parsed


def main() -> None:
    args = sys.argv[1:]
    if not args:
        usage()

    match args[0]:
        case "--reindex":
            if os.path.exists(db.DB_FILE):
                os.remove(db.DB_FILE)
            db.build()
            return
        case "--genres":
            ui.show_list(db.list_genres(), "GENRE", 40, "-g")
            return
        case "--langs":
            ui.show_list(db.list_langs(), "LANG", 10, "-l")
            return

    parsed     = _parse_args(args)
    flag       = parsed["flag"]
    query      = parsed["query"]
    lang       = parsed["lang"]
    download   = parsed["download"]
    extract_id = parsed["extract_id"]

    if extract_id is not None:
        entries = ui.resolve_by_spec(extract_id, cache.load())
        if not entries:
            print("Books not found.")
            sys.exit(1)
        for entry in entries:
            print(f"\n[{entry['AUTHOR']}] {entry['TITLE']}")
            downloader.extract(entry)
        return

    if flag is None:
        usage()

    if flag == "-s":
        series_list = db.search_series(query, lang=lang)
        ui.show_series(series_list, lang)
        return

    field_map = {"-a": "AUTHOR", "-t": "TITLE", "-g": "GENRE"}
    results   = db.search(field_map[flag], query, lang=lang)
    cache.save(results)

    if download is not None:
        entries = ui.resolve_by_spec(download, results)
        if not entries:
            print("Books not found.")
            sys.exit(1)
        for entry in entries:
            print(f"\n[{entry['AUTHOR']}] {entry['TITLE']}")
            downloader.extract(entry)
    else:
        ui.show_results(results)


if __name__ == "__main__":
    main()
