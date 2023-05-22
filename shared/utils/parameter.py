# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/19/2023 20:03
# @Author  : Tony Skywalker
# @File    : parameter.py
#
# Description:
#   Parameter adapter, convert request parameters into a dictionary.
#
from django.core.handlers.wsgi import WSGIRequest

from shared.utils.json_util import deserialize


def _parse_POST_param(request: WSGIRequest) -> dict:
    content_type:str = str(request.headers.get('Content-Type'))
    if content_type == 'application/json':
        return deserialize(request.body)
    elif content_type == 'application/x-www-form-urlencoded':
        return request.POST.dict()
    elif content_type.startswith('multipart/form-data'):
        return request.POST.dict()
    return {}


def _parse_GET_param(request: WSGIRequest) -> dict:
    return request.GET.dict()


def parse_param(request: WSGIRequest) -> dict:
    """
    This will not handle multipart/form-data request!
    :return: all parameters in dictionary
    """
    if request.method == 'POST':
        return _parse_POST_param(request)
    elif request.method == 'GET':
        return _parse_GET_param(request)
    return {}
