from pandas import DataFrame
from .data import get_book_data, get_user_data
import re


def parse_input_to_string_tuple(
    input: str,
) -> tuple[str, str | None, str | None, str | None] | None:
    cleaned = re.sub(r"\s+", " ", input)
    pattern = re.compile(
        r"(?P<book>(?:[123]\s)?\w+)(?:\s(?P<chapter>\d+)?(?::(?P<verse_start>\d+)(?:-(?P<verse_end>\d+))?)?)?"
    )
    match = pattern.match(cleaned)

    if match:
        return (
            match.group("book"),
            match.group("chapter"),
            match.group("verse_start"),
            match.group("verse_end"),
        )
    else:
        return None


def match_input_to_book(input_str: str, book_df: DataFrame) -> int | None:
    usx_match = book_df[book_df["usx_code"] == input_str]
    if not usx_match.empty:
        book_num: int = usx_match.iloc[0]["book_id"]
        return book_num
    name_match = book_df[book_df["book_name"] == input_str]
    if name_match.empty:
        return None
    book_num = name_match.iloc[0]["book_id"]
    return book_num


def tuple_to_verse_num(
    parsed_tuple: tuple[str, str | None, str | None, str | None] | None,
) -> tuple[int, int] | None:
    if parsed_tuple is None:
        return None
    book_data = get_book_data()
    user_data = get_user_data()
    book = match_input_to_book(parsed_tuple[0], book_data)
    chap = parsed_tuple[1]
    verse = parsed_tuple[2]
    verse_end = parsed_tuple[3]

    none_trig = False
    for item in (book, chap, verse, verse_end):
        if item is None:
            none_trig = True
        elif none_trig:
            return None

    result_set = user_data.copy()
    try:
        if book is not None:
            result_set = result_set[result_set["book_id"] == book]
            if chap is not None:
                result_set = result_set[result_set["chapter"] == chap]
                if verse is not None:
                    if verse_end is not None:
                        result_set = result_set[
                            result_set["verse"] >= verse
                            and result_set["verse"] <= verse_end
                        ]
                        max: int = result_set["verse_sequence"].max()
                        min: int = result_set["verse_sequence"].min()
                        return (min, max)
                    else:
                        # single verse
                        result: int = result_set[result_set["verse"] == verse].iloc[0][
                            "verse_sequence"
                        ]
                        return (result, result)
                else:
                    # whole chapter
                    max = result_set["verse_sequence"].max()
                    min = result_set["verse_sequence"].min()
                    return (min, max)
            else:
                # whole book
                max = result_set["verse_sequence"].max()
                min = result_set["verse_sequence"].min()
                return (min, max)
        else:
            return None
    except:
        return None
