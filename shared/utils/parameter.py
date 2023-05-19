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


def parse_param(request: WSGIRequest):
    """
    This will not handle multipart/form-data request!
    :return: all parameters in dictionary
    """
    content_type = request.headers.get('Content-Type')
    if content_type == 'application/json':
        return deserialize(request.body)
    if content_type == 'application/x-www-form-urlencoded':
        if request.method == 'POST':
            return request.POST.dict()
        elif request.method == 'GET':
            return request.GET.dict()
        return {}
    return {}
