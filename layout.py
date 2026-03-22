import shutil


AUTHOR_MIN: int = 14
AUTHOR_MAX: int = 35
TITLE_MIN:  int = 12
FALLBACK_W: int = 80
GAP:        int = 2

_NUM_W:  int = 4
_ID_W:   int = 8
_DATE_W: int = 11
_LANG_W: int = 4


def terminal_width() -> int:
    try:
        return shutil.get_terminal_size().columns
    except Exception:
        return FALLBACK_W


def _fit(s: str, w: int) -> str:
    if len(s) > w:
        return s[:w - 3] + "..."
    return s.ljust(w)


def _col_gap(n_cols: int) -> int:
    return (n_cols - 1) * GAP


class Layout:
    __slots__ = (
        "term_w", "num_w", "id_w", "author_w", "title_w", "date_w", "lang_w",
        "show_id", "total_w",
    )

    def __init__(self, term_w: int | None = None) -> None:
        self.term_w = (term_w if term_w is not None else terminal_width()) - 1
        self.num_w  = _NUM_W
        self.id_w   = _ID_W
        self.date_w = _DATE_W
        self.lang_w = _LANG_W
        self._compute()

    def _compute(self) -> None:
        w         = self.term_w
        fixed_sum = self.num_w + self.id_w + self.date_w + self.lang_w

        remainder = w - fixed_sum - _col_gap(6)

        if remainder < AUTHOR_MIN + TITLE_MIN:
            self.show_id = False
            remainder    = w - (fixed_sum - self.id_w) - _col_gap(5)
        else:
            self.show_id = True

        remainder = max(remainder, AUTHOR_MIN + TITLE_MIN)

        author_budget = min(AUTHOR_MAX, max(AUTHOR_MIN, remainder // 3))
        self.author_w = author_budget
        self.title_w  = max(TITLE_MIN, remainder - author_budget)

        widths       = self._col_widths()
        self.total_w = sum(widths) + _col_gap(len(widths))

    def _col_widths(self) -> list[int]:
        cols = [self.num_w, self.author_w, self.title_w, self.date_w, self.lang_w]
        if self.show_id:
            cols.insert(1, self.id_w)
        return cols

    def header_cells(self) -> list[str]:
        if self.show_id:
            return ["#", "ID", "AUTHOR", "TITLE", "DATE", "LANG"]
        return ["#", "AUTHOR", "TITLE", "DATE", "LANG"]

    def data_cells(
        self, num: str, fileid: str, author: str,
        title: str, date: str, lang: str,
    ) -> list[str]:
        if self.show_id:
            return [num, fileid, author, title, date, lang]
        return [num, author, title, date, lang]

    def row(self, cells: list[str]) -> str:
        sp     = " " * GAP
        widths = self._col_widths()
        padded = [_fit(c, w) for c, w in zip(cells, widths)]
        return sp.join(padded)
