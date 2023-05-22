# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/17/2023 16:40
# @Author  : Tony Skywalker
# @File    : json.py
#

class JsonException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f"JSON Error: {self.msg}"


class JsonSerializeException(JsonException):
    def __init__(self, msg, obj):
        super().__init__(msg)
        self.obj = obj

    def __str__(self):
        _str = super().__str__()
        _str += f"\n\tOn object: {'None' if self.obj is None else self.obj.__dict__}"
        return _str


class JsonDeserializeException(JsonException):
    def __init__(self, msg, obj):
        super().__init__(msg)
        self.obj = obj

    def __str__(self):
        _str = super().__str__()
        _str += f"\n\tOn string: {'None' if self.obj is None else self.obj}"
        return _str
