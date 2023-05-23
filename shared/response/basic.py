# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/18/2023 11:14
# @Author  : Tony Skywalker
# @File    : basic.py
#
# Description:
#   Basic responses.
#
from http import HTTPStatus

from shared.response.base import BaseResponse


class GoodResponse(BaseResponse):
    def __init__(self, dto):
        super().__init__(dto, HTTPStatus.OK)


class BadRequestResponse(BaseResponse):
    def __init__(self, dto):
        super().__init__(dto, HTTPStatus.OK)


class NotAuthorizedResponse(BaseResponse):
    def __init__(self, dto):
        super().__init__(dto, HTTPStatus.OK)


class ServerErrorResponse(BaseResponse):
    def __init__(self, dto):
        super().__init__(dto, HTTPStatus.INTERNAL_SERVER_ERROR)
