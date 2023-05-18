# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/17/2023 14:25
# @Author  : Tony Skywalker
# @File    : base.py
from PaperFives.settings import ERROR_CODE


class BaseResponseDto:
    def __init__(self, code, msg):
        self.code = code
        self.msg = msg


class GoodResponseDto(BaseResponseDto):
    def __init__(self, msg):
        super().__init__(ERROR_CODE['SUCCESS'], msg)
