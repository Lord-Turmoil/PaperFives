# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/22/2023 8:46
# @Author  : Tony Skywalker
# @File    : msgs.py
#
from datetime import datetime
from typing import List

from django.utils import timezone

from shared.dtos.models.base import BaseDto
from users.models import User


class BaseMessageDto(BaseDto):
    def __init__(self):
        self.uid: int = 0


class TextMessageDto(BaseMessageDto):
    class Payload:
        def __init__(self):
            self.text: str = ""

    def __init__(self):
        super().__init__()
        self.msg: TextMessageDto.Payload = TextMessageDto.Payload()


class LinkMessageDto(BaseMessageDto):
    class Payload:
        def __init__(self):
            self.text: str = ""
            self.link: str = ""

    def __init__(self):
        super().__init__()
        self.msg: LinkMessageDto.Payload = LinkMessageDto.Payload()


class ImageMessageDto(BaseMessageDto):
    def __init__(self):
        super().__init__()
        # it seems the form-data cannot send integer value. :(
        self.uid: str = ""


class ContactData(BaseDto):
    def __init__(self):
        super().__init__()
        self.uid: int = 0
        self.username: str = ''
        self.avatar: str = ''
        self.timestamp: datetime = timezone.now()
        self.unread: int = 0

    def init(self, user: User, timestamp, unread):
        self.uid = user.uid
        self.username = user.username
        self.avatar = user.avatar
        self.timestamp = timestamp
        self.unread = unread
        return self


class ContactListDto(BaseDto):
    def __init__(self):
        super().__init__()
        self.contacts: List[ContactData] = [ContactData()]

    def init(self, contacts):
        self.contacts = contacts
        return self
