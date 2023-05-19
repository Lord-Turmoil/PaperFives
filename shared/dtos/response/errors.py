# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/17/2023 14:27
# @Author  : Tony Skywalker
# @File    : error.py
#
from PaperFives.settings import ERROR_CODE
from shared.dtos.response.base import BaseResponseDto


class GeneralErrorDto(BaseResponseDto):
    """
    Will not provide detailed messages by default.
    """
    def __init__(self, code, msg="Not available"):
        super().__init__(code, msg)


class RequestMethodErrorDto(BaseResponseDto):
    def __init__(self, expect, actual):
        super().__init__(ERROR_CODE['WRONG_REQUEST_METHOD'], "401 Bad request")
        self.data = {'descr': f"'{expect}' expected but got '{actual}'"}


class BadRequestDto(BaseResponseDto):
    def __init__(self, hint="Not available"):
        super().__init__(ERROR_CODE['BAD_REQUEST'], "Request format error")
        self.data = {'descr': hint}


class ServerErrorDto(BaseResponseDto):
    def __init__(self, msg):
        super().__init__(ERROR_CODE['SERVER_ERROR'], msg)
