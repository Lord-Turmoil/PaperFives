# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/18/2023 8:42
# @Author  : Tony Skywalker
# @File    : base.py
#
from http import HTTPStatus

from django.http import HttpResponse

from shared.utils.json_util import serialize


class BaseResponse(HttpResponse):
    def __init__(self, dto, status=HTTPStatus.OK):
        super().__init__(serialize(dto), status=status)
