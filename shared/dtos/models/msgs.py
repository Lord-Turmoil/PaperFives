# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/22/2023 8:46
# @Author  : Tony Skywalker
# @File    : msgs.py
#
from datetime import datetime
from typing import List

from django.utils import timezone

from msgs.models import Message, TextPayload
from shared.dtos.models.base import BaseDto
from shared.utils.users.users import get_user_by_uid
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


class TextMessageData(BaseDto):
    def __init__(self):
        super().__init__()
        self.timestamp: datetime = timezone.now()
        self.text: str = ''
        self.income: bool = False
        self.avatar: str = ""

    def init(self, timestamp, text, income, avatar):
        self.timestamp = timestamp
        self.text = text
        self.income = income
        self.avatar = avatar
        return self


class TextMessageListDto(BaseDto):
    def __init__(self):
        super().__init__()
        self.msgs: List[TextMessageData] = [TextMessageData()]

    def init(self, src_uid, messages):
        self.msgs.clear()
        message: Message
        for message in messages:
            payloads = TextPayload.objects.filter(mid=message.mid)
            if not payloads.exists():
                continue
            payload: TextPayload = payloads.first()
            income = message.src_uid != src_uid
            user = get_user_by_uid(message.src_uid)
            if user is None:
                continue
            self.msgs.append(TextMessageData().init(message.timestamp, payload.text, income, user.avatar))
        return self
