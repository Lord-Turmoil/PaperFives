# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/27/2023 10:12
# @Author  : Tony Skywalker
# @File    : strict.py
#
# Description:
#   Response in this file will strictly return HTTP Status, with
# 'Http' prefix.
#

from http import HTTPStatus

from shared.response.base import BaseResponse


class HttpOKResponse(BaseResponse):
    def __init__(self, dto):
        super().__init__(dto, HTTPStatus.OK)


class HttpBadRequestResponse(BaseResponse):
    def __init__(self, dto):
        super().__init__(dto, HTTPStatus.BAD_REQUEST)


class HttpNotAuthorizedResponse(BaseResponse):
    def __init__(self, dto):
        super().__init__(dto, HTTPStatus.UNAUTHORIZED)


class HttpServerErrorResponse(BaseResponse):
    def __init__(self, dto):
        super().__init__(dto, HTTPStatus.INTERNAL_SERVER_ERROR)


class HttpPageNotFoundResponse(BaseResponse):
    def __init__(self, dto):
        super().__init__(dto, HTTPStatus.NOT_FOUND)
