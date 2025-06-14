import re
import pandas as pd
from .utils import parse_input_to_string_tuple, tuple_to_verse_num
import sys
from . import data


def get_read_date(reference: str) -> None:
    verse_tup = tuple_to_verse_num(parse_input_to_string_tuple(reference.strip()))
    if verse_tup is None:
        print(f"Verse reference {repr(reference)} not found.")
    else:
        print("Verse reference successfully parsed and found.")
        date = data.get_date(verse_tup[0])
        if date is None:
            print(f"{repr(reference)} has never been read.")
        else:
            print(f"{repr(reference)} was last read on {date.date()}")

def set_read_dates(verse_str: str, date_arg: str | int | None) -> None:
    verse_list = re.split(r"[;,]", verse_str)

    if isinstance(date_arg, str):
        try:
            read_date = pd.to_datetime(date_arg)
        except:
            print("Unable to parse date.", file=sys.stderr)
            return None
    elif date_arg is None:
        read_date = None
    else:
        today = pd.Timestamp.now()
        read_date = today - pd.Timedelta(days=date_arg)

    failures: list[str] = []
    success_cnt = 0
    for verse in verse_list:
        reference_tuple = parse_input_to_string_tuple(verse.strip())
        verse_range = tuple_to_verse_num(reference_tuple)
        date_str = read_date.date() if read_date is not None else "never"
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
                f"Successfully saved verse {verse_range[0]} as last read {date_str}"
            )
            success_cnt += 1
        else:
            print(
                f"Successfully parsed and identified user input '{verse.strip()}' as verse range {verse_range[0]}-{verse_range[1]}"
            )
            data.set_read_date(verse_range, read_date)
            print(
                f"Successfully saved verses {verse_range[0]}-{verse_range[1]} as last read {date_str}"
            )
            success_cnt += verse_range[1] - verse_range[0] + 1
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
