from dataclasses import dataclass


@dataclass(frozen=True)
class _Key:
    cmd:   str
    label: str

    def __str__(self) -> str:
        return f"{self.label}({self.cmd})"


NEXT        = _Key("n",  "Next page")
PREV        = _Key("p",  "Prev page")
GOTO        = _Key("g",  "Go to page")
BACK        = _Key("<",  "Back")
QUIT        = _Key("q",  "Quit")

SORT_ASC    = _Key("da", "Sort ↑")
SORT_DESC   = _Key("dd", "Sort ↓")
SORT_RESET  = _Key("dr", "Sort off")

LANG        = _Key("l",  "Language")
DOWNLOAD    = _Key("d",  "Download")
DOWNLOAD_ALL = _Key("dl", "Download all")

OPEN        = _Key("o",  "Open")
FILTER      = _Key("/",  "Filter")


def _line(*keys: _Key) -> str:
    return "  ".join(str(k) for k in keys)


def hints_results(has_parent: bool) -> str:
    keys = [NEXT, PREV, GOTO, SORT_ASC, SORT_DESC, SORT_RESET, LANG, DOWNLOAD, DOWNLOAD_ALL]
    if has_parent:
        keys.append(BACK)
    keys.append(QUIT)
    return _line(*keys)


def hints_series() -> str:
    return _line(NEXT, PREV, OPEN, DOWNLOAD, GOTO, QUIT)


def hints_list() -> str:
    return _line(NEXT, PREV, FILTER, QUIT)
