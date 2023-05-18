# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/18/2023 18:01
# @Author  : Tony Skywalker
# @File    : users.py
#
from django.core.handlers.wsgi import WSGIRequest

from shared.utils.token import verify_token
from users.models import User


def get_user_from_request(request: WSGIRequest):
    identity = request.META.get('HTTP_IDENTITY')
    token = request.META.get('HTTP_AUTHORIZATION')
    if not verify_token(identity, token):
        return None
    users = User.objects.filter(email=identity)
    if not users.exists():
        return None
    return users.first()
