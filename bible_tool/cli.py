from .core import set_read_dates, get_read_date
import argparse


def update(args: argparse.Namespace):
    if args.date is None:
        set_read_dates(args.reference, args.days_ago)
    else:
        set_read_dates(args.reference, args.date)


def delete(args: argparse.Namespace):
    confirm = input(
        f"Are you sure you want to set the date of last reading to null for {repr(args.reference)}? This cannot be undone (Y/n) "
    )
    if confirm.upper() == "Y":
        set_read_dates(args.reference, None)


def main():
    parser = argparse.ArgumentParser(
        description="Tool for tracking when Bible verses were last read."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # update command
    update_parser = subparsers.add_parser(
        "update",
        help="Update a verse's, range of verses', chapter's, or book's last read date",
    )
    update_parser.add_argument(
        "reference",
        help="Reference to the verse (Revelation 1:3), range of verses (Rev 1:1-5), chapter (Revelation 1), or book (REV) to be updated",
    )
    update_parser.add_argument(
        "--days_ago",
        "-a",
        type=int,
        default=0,
        help="Number of days before today that the reference was read",
    )
    update_parser.add_argument("--date", "-d", help="Date that the reference was read")
    update_parser.set_defaults(func=update)

    # Delete command
    update_parser = subparsers.add_parser(
        "delete",
        help="Set the last read date to null for specified Bible reference",
    )
    update_parser.add_argument(
        "reference",
        help="Reference to the verse (Revelation 1:3), range of verses (Rev 1:1-5), chapter (Revelation 1), or book (REV) to be set to null",
    )
    update_parser.set_defaults(func=delete)

    args = parser.parse_args()
    args.func(args)
