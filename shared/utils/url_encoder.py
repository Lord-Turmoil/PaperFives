# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/27/2023 9:38
# @Author  : Tony Skywalker
# @File    : url_encoder.py
#
# Description:
#   Convert string to URL format.
#

SAFE_CHARACTERS = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789-_~.'
REPLACEMENT = '_'


def convert_to_url(s: str) -> str:
    """
    Character except for Alphabets (A-Z a-z), Digits (0-9), hyphen (-), underscore (_) tilde (~),
    and dot (.) will be replaced by '_'
    """
    s = s.strip()
    ret = ""
    for i in range(len(s)):
        if s[i] in SAFE_CHARACTERS:
            ret += s[i]
        else:
            ret += REPLACEMENT
    return ret
