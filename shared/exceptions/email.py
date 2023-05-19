# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/18/2023 11:10
# @Author  : Tony Skywalker
# @File    : email.py
#


class EmailException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f"Failed to send msg: {self.msg}"
