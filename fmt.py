import re

from db import BookRow
from keys import hints_results
from layout import GAP, Layout, terminal_width


def format_date(date_str: str) -> str:
    try:
        p = date_str.split("-")
        if len(p) == 3:
            return f"{p[2]}-{p[1]}-{p[0]}"
    except Exception:
        pass
    return date_str


def format_author(raw: str) -> str:
    authors: list[str] = []
    for part in raw.split(":"):
        part = part.strip().strip(",")
        if not part:
            continue
        names = [n.strip() for n in part.split(",") if n.strip()]
        if not names:
            continue
        if len(names) == 1:
            authors.append(names[0])
        else:
            authors.append(" ".join(names[1:] + [names[0]]))
    return ", ".join(authors) if authors else raw


def author_for_filename(raw: str) -> str:
    for part in raw.split(":"):
        part = part.strip().strip(",")
        if not part:
            continue
        names = [n.strip() for n in part.split(",") if n.strip()]
        if not names:
            continue
        surname = names[0]
        initial = names[1][0] + "." if len(names) > 1 else ""
        return f"{initial}{surname}"
    return sanitize(raw)


def sanitize(s: str) -> str:
    return re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", s).strip()


def make_filename(entry: BookRow) -> str:
    author = sanitize(author_for_filename(entry["AUTHOR"]))[:40]
    title  = sanitize(re.sub(r"\s+", "-", entry["TITLE"].strip()))[:60]
    year   = entry["DATE"][:4] if entry["DATE"] else entry["FILEID"]
    return f"{author}_{title}_{year}.fb2"


def truncate(s: str, width: int) -> str:
    if len(s) <= width:
        return s
    return s[:width - 3] + "..."


SORT_LABELS: dict[str | None, str] = {
    None:   "default",
    "asc":  "↑ date",
    "desc": "↓ date",
}


def apply_sort(results: list[BookRow], sort: str | None) -> list[BookRow]:
    if sort == "asc":
        return sorted(results, key=lambda r: r["DATE"])
    if sort == "desc":
        return sorted(results, key=lambda r: r["DATE"], reverse=True)
    return results


def apply_lang(results: list[BookRow], lang: str | None) -> list[BookRow]:
    if not lang:
        return results
    return [r for r in results if r["LANG"] == lang]


def _status_line(page: int, total_pages: int, total: int,
                 sort: str | None, lang: str | None) -> str:
    sort_label = SORT_LABELS.get(sort, sort or "default")
    lang_label = lang if lang else "all"
    return (f"Page {page + 1}/{total_pages}"
            f"  |  Found: {total}"
            f"  |  Date: {sort_label}"
            f"  |  Lang: {lang_label}")


def print_page(
    results:    list[BookRow],
    page:       int,
    total:      int,
    sort:       str | None = None,
    lang:       str | None = None,
    page_size:  int        = 50,
    has_parent: bool       = False,
) -> None:
    lyt   = Layout()
    sp    = " " * GAP
    ruler = "─" * lyt.total_w

    total_pages = max(1, (total + page_size - 1) // page_size)
    start       = page * page_size
    end         = min(start + page_size, total)

    print(lyt.row(lyt.header_cells()))
    print(ruler)

    for i in range(start, end):
        r      = results[i]
        author = truncate(format_author(r["AUTHOR"]), lyt.author_w)
        title  = truncate(r["TITLE"], lyt.title_w)
        cells  = lyt.data_cells(
            str(i + 1),
            r["FILEID"],
            author,
            title,
            format_date(r["DATE"]),
            r["LANG"],
        )
        print(lyt.row(cells))

    print(ruler)
    print(_status_line(page, total_pages, total, sort, lang))
    print(hints_results(has_parent))
