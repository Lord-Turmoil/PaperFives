# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/22/2023 8:46
# @Author  : Tony Skywalker
# @File    : msgs.py
#
from shared.dtos.models.base import BaseDto


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



