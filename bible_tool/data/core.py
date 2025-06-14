import pandas as pd
import numpy as np
from pathlib import Path

current_dir = Path(__file__).parent


def reset_user() -> None:
    data = pd.read_csv(str(current_dir / "BibleData-Reference.csv"))
    user_data = data[["book_id", "chapter", "verse", "verse_sequence"]].copy()
    user_data["last_read"] = np.nan
    user_data.to_csv(str(current_dir / "user_data.csv"), index=False)


def reset_book() -> None:
    data = pd.read_csv(str(current_dir / "BibleData-Reference.csv"))
    book_data = data[["book_id", "usx_code"]].drop_duplicates()
    book_data["book_name"] = [
        # Old Testament
        "Genesis",
        "Exodus",
        "Leviticus",
        "Numbers",
        "Deuteronomy",
        "Joshua",
        "Judges",
        "Ruth",
        "1 Samuel",
        "2 Samuel",
        "1 Kings",
        "2 Kings",
        "1 Chronicles",
        "2 Chronicles",
        "Ezra",
        "Nehemiah",
        "Esther",
        "Job",
        "Psalms",
        "Proverbs",
        "Ecclesiastes",
        "Song of Solomon",
        "Isaiah",
        "Jeremiah",
        "Lamentations",
        "Ezekiel",
        "Daniel",
        "Hosea",
        "Joel",
        "Amos",
        "Obadiah",
        "Jonah",
        "Micah",
        "Nahum",
        "Habakkuk",
        "Zephaniah",
        "Haggai",
        "Zechariah",
        "Malachi",
        # New Testament
        "Matthew",
        "Mark",
        "Luke",
        "John",
        "Acts",
        "Romans",
        "1 Corinthians",
        "2 Corinthians",
        "Galatians",
        "Ephesians",
        "Philippians",
        "Colossians",
        "1 Thessalonians",
        "2 Thessalonians",
        "1 Timothy",
        "2 Timothy",
        "Titus",
        "Philemon",
        "Hebrews",
        "James",
        "1 Peter",
        "2 Peter",
        "1 John",
        "2 John",
        "3 John",
        "Jude",
        "Revelation",
    ]

    book_data.to_csv(str(current_dir / "book_data.csv"), index=False)


def reset_data() -> None:
    reset_user()
    reset_book()


def get_user_data() -> pd.DataFrame:
    user_path = current_dir / "user_data.csv"
    if not user_path.exists():
        print(f"File {user_path} not found. Repairing...")
        reset_user()
        print(f"File {user_path} successfully repaired.")
    return pd.read_csv(str(user_path), parse_dates=["last_read"])


def get_book_data() -> pd.DataFrame:
    book_path = current_dir / "book_data.csv"
    if not book_path.exists():
        print(f"File {book_path} not found. Repairing...")
        reset_book()
        print(f"File {book_path} successfully repaired.")
    return pd.read_csv(str(book_path))

def get_date(verse_num: int) -> pd.Timestamp | None:
    df = get_user_data()
    date: pd.Timestamp | None = df[df["verse_sequence"] == verse_num]["last_read"][0]
    return date

def set_read_date(verse_range: tuple[int, int], date_read: pd.Timestamp | None) -> None:
    df = get_user_data()
    df.loc[
        (df["verse_sequence"] >= verse_range[0]) & (df["verse_sequence"] <= verse_range[1]),
        "last_read",
    ] = date_read
    df.to_csv(str(current_dir / "user_data.csv"), index=False, date_format="%Y-%m-%d")
