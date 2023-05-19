# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/18/2023 14:26
# @Author  : Tony Skywalker
# @File    : user.py
#

from PaperFives.settings import ERROR_CODE
from shared.dtos.response.base import BaseResponseDto, GoodResponseDto


class NotAuthorizedDto(BaseResponseDto):
    def __init__(self, msg):
        super().__init__(ERROR_CODE['NOT_AUTHORIZED'], msg)


class AlreadyLoggedInDto(BaseResponseDto):
    def __init__(self):
        super().__init__(ERROR_CODE['ALREADY_LOGGED_IN'], "Already logged in")


class NoSuchUserDto(BaseResponseDto):
    def __init__(self):
        super().__init__(ERROR_CODE['NO_SUCH_USER'], "Whom are you looking for?")


class WrongPasswordDto(BaseResponseDto):
    def __init__(self):
        super().__init__(ERROR_CODE['WRONG_PASSWORD'], "Wrong password")


class LoginSuccessDto(GoodResponseDto):
    """
    When logged in, server will return complete user info, and the
    corresponding login token.
    {
        "code": 0,
        "msg": "...",
        "user": {
            "uid": 123,
            "email": "...",
            "username": "...",
            "avatar": "/static/avatar/13213213.png",
            "attr": {
                "sex": 0            (int in [0, 1, 2])
                "institute": "...", (may be empty)
            }
            "stat": {
                "publish_cnt": 123,
                "message_cnt": 456
            }
        },
        "token": {
            "identity": "...",
            "token": "..."
        }
    """

    def __init__(self, user):
        """
        user and token are all dict object.
        """
        super().__init__("Welcome back to PaperFives!")
        self.user = user


class UserProfileDto(GoodResponseDto):
    def __init__(self, data):
        super().__init__()
        self.user = data


class NotLoggedInDto(BaseResponseDto):
    def __init__(self):
        super().__init__(ERROR_CODE['NOT_LOGGED_IN'], "Please login first.")
       