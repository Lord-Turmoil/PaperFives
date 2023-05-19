# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/17/2023 14:25
# @Author  : Tony Skywalker
# @File    : base.py
from PaperFives.settings import ERROR_CODE


class BaseResponseDto:
    def __init__(self, code, msg="Not available"):
        self.meta = {'status': code, 'msg': msg }
        self.data = {}


class GoodResponseDto(BaseResponseDto):
    def __init__(self, msg="Not available"):
        super().__init__(ERROR_CODE['SUCCESS'], msg)
