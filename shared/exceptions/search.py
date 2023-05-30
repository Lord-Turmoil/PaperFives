# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/29/2023 16:36
# @Author  : Tony Skywalker
# @File    : search.py
#

class SearchErrorException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f"Search Error: {self.msg}"
