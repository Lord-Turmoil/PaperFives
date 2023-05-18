# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/17/2023 14:27
# @Author  : Tony Skywalker
# @File    : error.py
#
from PaperFives.settings import ERROR_CODE
from shared.dtos.base import BaseDto


class RequestMethodErrorDto(BaseDto):
    def __int__(self, expect, actual):
        super().__init__(ERROR_CODE['WRONG_REQUEST_METHOD'], "401 Bad request")
        self.descr = f"'{expect}' expected but got '{actual}'"


class BadRequestDto(BaseDto):
    def __init__(self, hint="not available"):
        super().__init__(ERROR_CODE['BAD_REQUEST'], "Request format error")
        self.hint = hint

class GeneralErrorDto(BaseDto):
    def __int__(self, code, msg):
        super().__int__(code)
        