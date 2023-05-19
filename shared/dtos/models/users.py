# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/17/2023 16:54
# @Author  : Tony Skywalker
# @File    : user.py
#
from shared.dtos.models.base import BaseDto
from shared.utils.str_util import is_null_or_empty, is_no_content
from users.models import UserAttribute, User


class UserAttrDto(BaseDto):
    def __init__(self):
        self.sex: int = 0
        self.institute: str = ""

    def is_valid(self) -> bool:
        if self.sex not in UserAttribute.Sex.values:
            return False
        if is_no_content(self.institute):
            return False
        return True


class UserDto(BaseDto):
    def __init__(self):
        self.email: str = ""
        self.username: str = ""
        self.attr: UserAttrDto = UserAttrDto()

    def is_valid(self) -> bool:
        if is_no_content(self.email) or is_no_content(self.username):
            return False
        if self.attr is None:
            return False
        return self.attr.is_valid()


class RegisterDto(BaseDto):
    def __init__(self):
        self.email: str = ""
        self.username: str = ""
        self.password: str = ""
        self.code: str = ""

class LoginDto(BaseDto):
    def __init__(self):
        self.email: str = ""
        self.password: str = ""
