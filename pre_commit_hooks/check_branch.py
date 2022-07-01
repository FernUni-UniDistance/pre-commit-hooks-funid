from __future__ import annotations

import os.path
import git
from git import Repo
from git import Git


def check_up_to_date(mis_match):
    """checks if the local repo and branch 
    is up to date or not """
    directory = os.getcwd()
    repo = Repo(directory)
    for data in repo.remote().fetch("--dry-run"):
        # Reference: https://gitpython.readthedocs.io/en/stable/reference.html
        # Possible values for data.flags
        # > ERROR= 128
        # > FAST_FORWARD= 64
        # > FORCED_UPDATE= 32
        # > HEAD_UPTODATE= 4
        # > NEW_HEAD= 2
        # > NEW_TAG= 1
        # > REJECTED= 16
        # > TAG_UPDATE= 8
        if data.flags != 4 and (data.remote_ref_path).strip() == "13.0":
            mis_match = True
            print(
                f'[FD813].'
                f'Your local repository is not up'
                f'to date with production repository'
            )
    # Compare historical of commits with remotes/origin/13.0
    if repo.git.rev_list("..remotes/origin/13.0"):
        mis_match = True
        print(
            f'[FD813].'
            f'Your branch is not up to date with origin/13.0'
        )
    return mis_match


def main():
    mis_match = False
    mis_match = check_up_to_date(mis_match)
    return mis_match
