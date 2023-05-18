# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/17/2023 16:54
# @Author  : Tony Skywalker
# @File    : user.py
#
from PaperFives.settings import ERROR_CODE
from shared.dtos.base import BaseDto
from shared.utils.str_util import is_null_or_empty, is_no_content
from users.models import UserAttribute


class UserAttrDto:
    def __init__(self):
        self.sex: int = 0
        self.institute: str = ""

    def is_valid(self) -> bool:
        if self.sex not in UserAttribute.Sex.choices:
            return False
        if is_null_or_empty(self.institute):
            return False
        return True


class UserDto:
    def __init__(self):
        self.email: str = ""
        self.username: str = ""
        self.attr: UserAttrDto = UserAttrDto()

    def is_valid(self) -> bool:
        if is_null_or_empty(self.email) or is_null_or_empty(self.username):
            return False
        if self.attr is None:
            return False
        return self.attr.is_valid()


class RegisterDto:
    def __init__(self):
        self.email: str = ""
        self.username: str = ""
        self.code: str = ""
        self.password: str = ""

    def is_valid(self) -> bool:
        for key in self.__dict__.keys():
            if is_no_content(self.__dict__[key]):
                return False
        return True


class CreateUserFailedDto(BaseDto):
    def __init__(self):
        super().__init__(ERROR_CODE['CREATE_USER'], "Failed to create user")


class CreateUserSucceededDto(BaseDto):
    def __init__(self):
        super().__init__(ERROR_CODE['SUCCESS'], "User created!")
