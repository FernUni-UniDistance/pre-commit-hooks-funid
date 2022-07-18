from __future__ import annotations
import argparse
import polib
import os.path
import re
from typing import Sequence
from collections import Counter


def emptypo():
    po_obj = polib.POFile()
    po_obj.metadata = {
        "Project-Id-Version": "Odoo Server 13.0+e",
        "Report-Msgid-Bugs-To": "",
        "POT-Creation-Date": "2020-03-26 15:18+0000",
        "PO-Revision-Date": "2020-03-26 15:18+0000",
        "Last-Translator": "",
        "Language-Team": "",
        "MIME-Version": "1.0",
        "Content-Type": "text/plain; charset=UTF-8",
        "Content-Transfer-Encoding": "",
        "Plural-Forms": "",
    }
    return po_obj


def search_duplicate_menu(filename, duplicate):
    """ search for duplicate menu and window action"""
    with open(filename, 'rb') as f:
        duplicate = duplicate
        file = f.readlines()
        set_file = set(file)
        expressions = ("^#: model:ir.ui.menu",
                       "^#: model:ir.actions.act_window")
        for line in set_file:
            for exp in expressions:
                if re.search(exp, line.decode("utf-8")):
                    indices = [index + 1 for (index, item) in enumerate(file)
                               if item == line]
                    if len(indices) > 1:
                        if exp == "^#: model:ir.ui.menu":
                            selection = "Menu"
                            code = "DM8103"
                        else:
                            selection = "Window Action"
                            code = "DWA8103"
                        print(
                            f'[{code}].'
                            f'Duplicate {selection} on {filename}'
                            f'(on lines {indices}).',
                        )
                        duplicate = True
    return duplicate


def sort_entries(po_file_path, duplicate, save=False):
    """
    Sort a po file
    :rtype: object
    if sorted will check for duplicates
    """
    po_file = polib.pofile(po_file_path)
    po_out = emptypo()
    for entry in sorted(po_file, key=lambda x: x.msgid):
        po_out.append(entry)
    if po_out != po_file and save:
        file_name = po_file_path
        print("[FS8013] File Sorted", file_name)
        po_out.save(file_name)
        return True
    return search_duplicate_menu(po_file_path, duplicate)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)
    duplicate = False
    for filename in args.filenames:
        base = os.path.basename(filename)
        if re.search(".po$", base):
            duplicate = sort_entries(filename, duplicate, True)

    return duplicate


if __name__ == "__main__":
    raise SystemExit(main())
