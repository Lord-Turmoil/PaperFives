# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/16/2023 22:13
# @Author  : Tony Skywalker
# @File    : str_util.py
#
# Description:
#   This util file is as a replacement for some useful native string
# support in C#.
#

def is_null_or_empty(s: str) -> bool:
    if s is None:
        return True
    if isinstance(s, str) and len(s) == 0:
        return True
    return False


def is_no_content(s: str) -> bool:
    if is_null_or_empty(s):
        return True
    return s.isspace()


def make_not_null(s: str) -> bool:
    if is_null_or_empty(s):
        s = ""
        return True
    return False
