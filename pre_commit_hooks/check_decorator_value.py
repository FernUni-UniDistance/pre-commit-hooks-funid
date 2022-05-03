from __future__ import annotations

import argparse
import re
import os.path
from typing import Sequence


def check_decorator(src: bytes,missing_tag,filename: str = '<unknown>') -> int:
    file = src.readlines()
    missing_tag = missing_tag
    lastline = ""
    for line in file:
        if re.search("^class.*:$", line.decode("utf-8")):
            if (
                lastline == ""
                or ('funid_test' not in lastline )
            ):
                index = file.index(line)
                print(
                    f'[CD813].'
                    f'{filename}:  missing tag "funid_test"'
                    f'(on line {index}).',
                )
                missing_tag = True

        lastline = line.decode("utf-8")
    return missing_tag


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args(argv)
    missing_tag = False
    for filename in args.filenames:
        base = os.path.basename(filename)
        if (
                re.match("^test.*py$", base) and
                base != '__init__.py' 
        ):
            with open(filename, 'rb') as f:
                missing_tag = check_decorator(
                    f, missing_tag, filename=filename
                )
    return missing_tag
