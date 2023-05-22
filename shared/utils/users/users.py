# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/18/2023 18:01
# @Author  : Tony Skywalker
# @File    : users.py
#
from django.core.handlers.wsgi import WSGIRequest

from users.models import User


def get_user_from_request(request: WSGIRequest):
    uid = request.session.get('uid')
    if uid is None:
        return None
    users = User.objects.filter(uid=uid)
    if users.exists():
        return users.first()
    return None

def get_user_by_uid(uid):
    users = User.objects.filter(uid=uid)
    if users.exists():
        return users.first()
    return None

