# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/18/2023 18:01
# @Author  : Tony Skywalker
# @File    : users.py
#
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet

from shared.utils.token import get_identity_from_token, verify_token
from shared.utils.users.roles import is_user_admin
from users.models import User


def _get_user_from_session(request: WSGIRequest):
    uid = request.session.get('uid')
    if uid is None:
        return None
    users = User.objects.filter(uid=uid)
    if users.exists():
        return users.first()
    return None


def _get_user_from_jwt(request: WSGIRequest):
    token = request.META.get('HTTP_AUTHORIZATION', None)
    if not verify_token(token):  # None will be checked
        return None
    uid = get_identity_from_token(token)
    if uid is None:
        return None
    users = User.objects.filter(uid=uid)
    if users.exists():
        return users.first()
    return None


def get_user_from_request(request: WSGIRequest):
    return _get_user_from_jwt(request)


def get_admin_from_request(request: WSGIRequest):
    user = get_user_from_request(request)
    if user is None:
        return None
    if is_user_admin(user):
        return user
    return None


def get_user_by_uid(uid):
    users = User.objects.filter(uid=uid)
    if users.exists():
        return users.first()
    return None


def get_user_by_email(email):
    users = User.objects.filter(email=email)
    if users.exists():
        return users.first()
    return None


def get_users_by_username(username: str) -> QuerySet:
    users = User.objects.filter(username=username)
    return users
