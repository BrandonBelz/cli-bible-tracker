import re
import pandas as pd
from .utils import parse_input_to_string_tuple, tuple_to_verse_num
import sys
from . import data


def set_read_dates(verse_str: str, read_date: pd.Timestamp) -> None:
    verse_list = re.split(r"[;,]", verse_str)

    failures: list[str] = []
    success_cnt = 0
    for verse in verse_list:
        verse_range = tuple_to_verse_num(parse_input_to_string_tuple(verse.strip()))
        if verse_range is None:
            print(
                f"error: failed to parse and identify user input '{verse.strip()}'",
                file=sys.stderr,
            )
            failures.append(verse.strip())
        elif verse_range[0] == verse_range[1]:
            print(
                f"Successfully parsed and identified user input '{verse.strip()}' as verse number {verse_range[0]}"
            )
            data.set_read_date(verse_range, read_date)
            print(
                f"Successfully saved verse {verse_range[0]} as last read on {read_date.date()}"
            )
            success_cnt += 1
        else:
            print(
                f"Successfully parsed and identified user input '{verse.strip()}' as verse range {verse_range[0]}-{verse_range[1]}"
            )
            data.set_read_date(verse_range, read_date)
            print(
                f"Successfully saved verses {verse_range[0]}-{verse_range[1]} as last read on {read_date.date()}"
            )
            success_cnt += verse_range[1] - verse_range[0] + 1
    print()
    if len(failures) == 0:
        print(f"Success! {success_cnt} verses updated.")
    else:
        print("Task completed with errors.", file=sys.stderr)
        for verse in verse_list:
            print(
                f"\terror: failed to parse and identify user input '{verse.strip()}'",
                file=sys.stderr,
            )
        print(
            f"{success_cnt} verses successfully updated. Errors encountered in parsing and identifying user input. See above for details."
        )
