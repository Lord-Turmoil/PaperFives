# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/23/2023 23:30
# @Author  : Tony Skywalker
# @File    : parser.py
#
# Description:
#   To parse values.
#

def parse_value(val, _type):
    try:
        return _type(val)
    except:
        return None