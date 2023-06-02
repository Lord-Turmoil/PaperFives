# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/23/2023 23:30
# @Author  : Tony Skywalker
# @File    : parser.py
#
# Description:
#   To parse values.
#
import datetime


def parse_value(val, _type, default=None):
    if val is None:
        return default
    try:
        if issubclass(_type, datetime.datetime):
            if isinstance(val, str):
                return datetime.datetime.strptime(val, '%Y-%m-%d %H:%M:%S')
            else:
                return default
        elif issubclass(_type, datetime.date):
            if isinstance(val, str):
                return datetime.datetime.strptime(val, '%Y-%m-%d')
            else:
                return default
        else:
            return _type(val)
    except ValueError:
        return default
