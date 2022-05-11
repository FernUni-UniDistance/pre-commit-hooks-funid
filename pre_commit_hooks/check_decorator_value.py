from __future__ import annotations

import argparse
import re
import os.path
from typing import Sequence


def check_decorator(src: bytes,missing_tag,filename: str = '<unknown>') -> int:
    file = src.readlines()
    missing_tag = missing_tag
    last_line = ""
    for line in file:
        if re.search("^class.*:$", line.decode("utf-8")):
            if (
                last_line == ""
                or ('"funid_test"' not in last_line and
                    "'funid_test'" not in last_line)
            ):
                index = file.index(line)
                print(
                    f'[CD813].'
                    f'{filename}:  missing tag "funid_test"'
                    f'(on line {index}).',
                )
                missing_tag = True

        last_line = line.decode("utf-8")
    return missing_tag


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)
    missing_tag = False
    for filename in args.filenames:
        dir = os.path.dirname(filename).split('/')
        if 'tests' in dir:
            base = os.path.basename(filename)
            if (
                    re.match("^test.*py$", base) or
                    base == 'common.py'
            ):
                with open(filename, 'rb') as f:
                    missing_tag = check_decorator(
                        f, missing_tag, filename=filename
                    )
    return missing_tag
