from .reset import reset_user, reset_book
from pandas import DataFrame, read_csv
from .reset import main as reset_all

def get_user_info() -> DataFrame | None:
    try:
        return read_csv("user_data.csv")
    except:
        reset_user()
        return None

def get_book_info() -> DataFrame | None:
    try:
        return read_csv("book_data")
    except:
        reset_book()
        return None
