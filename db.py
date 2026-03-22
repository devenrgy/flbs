import glob
import os
import re
import sqlite3
import zipfile
from typing import Any

from config import DB_FILE, FLIBUSTA_PATH, INDEX_DIR, INPX_NAME


BookRow = dict[str, str]


def connect() -> sqlite3.Connection:
    con = sqlite3.connect(DB_FILE)
    con.row_factory = sqlite3.Row
    return con


def _row_to_dict(row: sqlite3.Row) -> BookRow:
    return {
        "FILEID":   row["fileid"],
        "FILENAME": row["filename"],
        "AUTHOR":   row["author"],
        "GENRE":    row["genre"],
        "TITLE":    row["title"],
        "SERIES":   row["series"],
        "SERNO":    row["serno"],
        "SIZE":     row["size"],
        "LIBID":    row["libid"],
        "DEL":      row["del"],
        "EXT":      row["ext"],
        "DATE":     row["date"],
        "LANG":     row["lang"],
        "KEYWORDS": row["keywords"],
    }


def build() -> None:
    inpx = os.path.join(FLIBUSTA_PATH, INPX_NAME)
    if not os.path.isdir(INDEX_DIR):
        print(f"Extracting index from {inpx} ...")
        with zipfile.ZipFile(inpx, "r") as z:
            z.extractall(INDEX_DIR)

    print("Building SQLite index (one-time, ~1-2 min) ...")
    con = connect()
    con.executescript("""
        CREATE TABLE IF NOT EXISTS books (
            fileid   TEXT PRIMARY KEY,
            filename TEXT,
            author   TEXT,
            genre    TEXT,
            title    TEXT,
            series   TEXT,
            serno    TEXT,
            size     TEXT,
            libid    TEXT,
            del      TEXT,
            ext      TEXT,
            date     TEXT,
            lang     TEXT,
            keywords TEXT
        );
        CREATE INDEX IF NOT EXISTS idx_author ON books(author COLLATE NOCASE);
        CREATE INDEX IF NOT EXISTS idx_title  ON books(title  COLLATE NOCASE);
        CREATE INDEX IF NOT EXISTS idx_genre  ON books(genre  COLLATE NOCASE);
        CREATE INDEX IF NOT EXISTS idx_series ON books(series COLLATE NOCASE);
        CREATE INDEX IF NOT EXISTS idx_lang   ON books(lang);
    """)

    total = 0
    for inp_path in sorted(glob.glob(os.path.join(INDEX_DIR, "*.inp"))):
        inp_name = os.path.basename(inp_path)
        file7z   = re.sub(r"\.inp$", ".7z", inp_name)
        rows: list[tuple[Any, ...]] = []
        with open(inp_path, encoding="utf-8", errors="replace") as f:
            for line in f:
                p = line.rstrip("\n").split("\x04")
                while len(p) < 13:
                    p.append("")
                fileid = p[5].strip()
                if not fileid:
                    continue
                rows.append((
                    fileid, file7z,
                    p[0].strip(), p[1].strip(), p[2].strip(),
                    p[3].strip(), p[4].strip(), p[6].strip(),
                    p[7].strip(), p[8].strip(), p[9].strip(),
                    p[10].strip(), p[11].strip(),
                    p[12].strip() if len(p) > 12 else "",
                ))
        con.executemany("""
            INSERT OR IGNORE INTO books
            (fileid,filename,author,genre,title,series,serno,size,libid,del,ext,date,lang,keywords)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, rows)
        con.commit()
        total += len(rows)
        print(f"  {inp_name}: {len(rows)} records", end="\r")

    con.close()
    print(f"\nDone. Indexed: {total} books.")


def is_ready() -> bool:
    if not os.path.exists(DB_FILE):
        return False
    try:
        con = connect()
        n = con.execute("SELECT COUNT(*) FROM books").fetchone()[0]
        con.close()
        return n > 0
    except Exception:
        return False


def ensure() -> None:
    if not is_ready():
        build()


def search(field: str, query: str, lang: str | None = None) -> list[BookRow]:
    ensure()
    col_map = {"AUTHOR": "author", "TITLE": "title", "GENRE": "genre", "SERIES": "series"}
    col     = col_map.get(field, "title")
    sql     = f"SELECT * FROM books WHERE {col} LIKE ? COLLATE NOCASE"
    params: list[str] = [f"%{query}%"]
    if lang:
        sql += " AND lang = ?"
        params.append(lang)
    sql += " ORDER BY date DESC"
    con  = connect()
    rows = con.execute(sql, params).fetchall()
    con.close()
    return [_row_to_dict(r) for r in rows]


def search_by_id(fileid: str) -> BookRow | None:
    ensure()
    con = connect()
    row = con.execute("SELECT * FROM books WHERE fileid = ?", (fileid,)).fetchone()
    con.close()
    return _row_to_dict(row) if row else None


def search_series(query: str, lang: str | None = None) -> list[tuple[str, int]]:
    ensure()
    sql     = ("SELECT series, COUNT(*) as cnt FROM books "
               "WHERE series LIKE ? COLLATE NOCASE AND series != ''")
    params: list[str] = [f"%{query}%"]
    if lang:
        sql += " AND lang = ?"
        params.append(lang)
    sql += " GROUP BY series ORDER BY series"
    con  = connect()
    rows = con.execute(sql, params).fetchall()
    con.close()
    return [(r["series"], r["cnt"]) for r in rows]


def search_books_in_series(series_name: str, lang: str | None = None) -> list[BookRow]:
    ensure()
    sql     = "SELECT * FROM books WHERE series = ? COLLATE NOCASE"
    params: list[str] = [series_name]
    if lang:
        sql += " AND lang = ?"
        params.append(lang)
    sql += " ORDER BY CAST(serno AS INTEGER), date"
    con  = connect()
    rows = con.execute(sql, params).fetchall()
    con.close()
    return [_row_to_dict(r) for r in rows]


def list_genres() -> list[tuple[str, int]]:
    ensure()
    con  = connect()
    rows = con.execute("""
        SELECT genre, COUNT(*) as cnt FROM books
        WHERE genre != '' GROUP BY genre ORDER BY cnt DESC
    """).fetchall()
    con.close()
    return [(r["genre"], r["cnt"]) for r in rows]


def list_langs() -> list[tuple[str, int]]:
    ensure()
    con  = connect()
    rows = con.execute("""
        SELECT lang, COUNT(*) as cnt FROM books
        WHERE lang != '' GROUP BY lang ORDER BY cnt DESC
    """).fetchall()
    con.close()
    return [(r["lang"], r["cnt"]) for r in rows]
