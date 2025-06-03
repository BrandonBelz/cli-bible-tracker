import pandas as pd
import numpy as np
from pathlib import Path

current_dir = Path(__file__).parent


def reset_user() -> None:
    data = pd.read_csv(str(current_dir / "BibleData-Reference.csv"))
    user_data = data[["book_id", "chapter", "verse"]].copy()
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
        reset_user()
    return pd.read_csv(str(user_path))


def get_book_data() -> pd.DataFrame:
    book_path = current_dir / "book_data.csv"
    if not book_path.exists():
        reset_book()
    return pd.read_csv(str(book_path))
