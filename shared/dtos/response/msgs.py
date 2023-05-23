# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/22/2023 9:01
# @Author  : Tony Skywalker
# @File    : msgs.py
#
import datetime

from django.utils import timezone

from PaperFives.settings import ERROR_CODE
from msgs.models import TextPayload, LinkPayload, ImagePayload, Message
from shared.dtos.response.base import GoodResponseDto, BaseResponseDto


class BaseMessageResponseData:
    def __init__(self, _src, _dst, _type, _timestamp):
        self.src: int = _src
        self.dst: int = _dst
        self.type: int = _type
        self.timestamp: datetime = _timestamp


class TextMessageResponseData(BaseMessageResponseData):
    class Payload:
        def __init__(self, _text):
            self.text: str = _text

    def __init__(self, _src, _dst, _timestamp, payload: TextPayload):
        super().__init__(_src, _dst, Message.MessageType.TEXT, _timestamp)
        self.msg: TextMessageResponseData.Payload = TextMessageResponseData.Payload(payload.text)


class LinkMessageResponseData(BaseMessageResponseData):
    class Payload:
        def __init__(self, _text: str, _link: str):
            self.text: str = _text
            self.link: str = _link

    def __init__(self, _src, _dst, _timestamp, payload: LinkPayload):
        super().__init__(_src, _dst, Message.MessageType.LINK, _timestamp)
        self.msg: LinkMessageResponseData.Payload = LinkMessageResponseData.Payload(payload.text, payload.link)


class ImageMessageResponseData(BaseMessageResponseData):
    class Payload:
        def __init__(self, _url: str, **kwargs):
            self.url: str = _url

    def __init__(self, _src, _dst, _timestamp, payload: ImagePayload):
        super().__init__(_src, _dst, Message.MessageType.IMAGE, _timestamp)
        self.msg: ImageMessageResponseData.Payload = ImageMessageResponseData.Payload(payload.path)


class MessageResponseDto(GoodResponseDto):
    def __init__(self, msg):
        super().__init__(data={'content': msg})


class MessageSelfErrorDto(BaseResponseDto):
    def __init__(self):
        super().__init__(ERROR_CODE['MESSAGE_SELF'], "You can't send message to yourself!")
