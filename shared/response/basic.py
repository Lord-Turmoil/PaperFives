# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/18/2023 11:14
# @Author  : Tony Skywalker
# @File    : basic.py
#
# Description:
#   Basic responses.
#
from shared.response.base import BaseResponse
from http import HTTPStatus


class GoodResponse(BaseResponse):
    def __init__(self, dto):
        super().__init__(dto, HTTPStatus.BAD_REQUEST)


class BadRequestResponse(BaseResponse):
    def __init__(self, dto):
        super().__init__(dto, HTTPStatus.BAD_REQUEST)


class NotAuthorizedResponse(BaseResponse):
    def __init__(self, dto):
        super().__init__(dto, HTTPStatus.UNAUTHORIZED)
