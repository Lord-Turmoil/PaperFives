# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/17/2023 14:27
# @Author  : Tony Skywalker
# @File    : error.py
#
from PaperFives.settings import ERROR_CODE
from shared.dtos.base import BaseResponseDto


class RequestMethodErrorDto(BaseResponseDto):
    def __int__(self, expect, actual):
        super().__init__(ERROR_CODE['WRONG_REQUEST_METHOD'], "401 Bad request")
        self.descr = f"'{expect}' expected but got '{actual}'"


class BadRequestDto(BaseResponseDto):
    def __init__(self, hint):
        super().__init__(ERROR_CODE['BAD_REQUEST'], "What a bad request")
        self.hint = hint
