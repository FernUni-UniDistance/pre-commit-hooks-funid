from __future__ import annotations

import os.path
import git
from git import Repo
from git import Git


def check_remote(mis_match):
    """ to check if remote upstream is set ,
        to check if upstream is equal to FernUni Repo
        and ti check if origin not equal to FernUni Repo
    """
    g = git.cmd.Git()
    try:
        g.ls_remote('upstream').split('\n')
    except Exception:
        # exception occurs when there is no remote named 'upstream'
        print(
            f'[AUR813].'
            f'You seem not to have an upstream remote'
        )
        mis_match = True
        return mis_match
    if (g.remote('get-url', 'origin') ==
            'https://github.com/FernUni-UniDistance/FSCH.git'):
        print(
            f'[FOR813].'
            f'Remote origin is pointing to FernUni'
            f'repository and should be linked to your Fork url'
        )
        mis_match = True
    if (g.remote('get-url', 'upstream') !=
            'https://github.com/FernUni-UniDistance/FSCH.git'):
        print(
            f'[FUS813].'
            f'Your upstream remote is '
            f'not the FernUni repository'
        )
        mis_match = True
    return mis_match


def check_up_to_date(mis_match):
    """checks if the local repo and branch 
    is up to date or not """
    directory = os.getcwd()
    repo = Repo(directory)
    try:
        for data in repo.remote('upstream').fetch("--dry-run"):
            # Reference:
            # https://gitpython.readthedocs.io/en/stable/reference.html
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
        # Compare historical of commits with remotes/upstream/13.0
        if repo.git.rev_list("..remotes/upstream/13.0"):
            mis_match = True
            print(
                f'[FD813].'
                f'Your branch is not up to date with upstream/13.0'
            )
        return mis_match
    except Exception:
        # exception occur when you do not  have a remote 'upstream'
        # or when you have created the upstream
        # but have not done fetch operation
        print(
            f'[AUR813]'
            f'You seem not to have an upstream remote '
            f'OR seem not to have done a fetch'
        )
        mis_match = True
        return mis_match


def main():
    mis_match = False
    mis_match = check_up_to_date(mis_match)
    return mis_match
