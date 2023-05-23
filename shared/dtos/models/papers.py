# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/23/2023 14:56
# @Author  : Tony Skywalker
# @File    : paper_data.py
#
# Description:
#   Dto for all paper properties.
#
# Warning:
#   For now, there are no check for validity. :(
#

from datetime import datetime
from typing import List

from shared.dtos.models.base import BaseDto
from shared.utils.parser import parse_value
from shared.utils.str_util import is_no_content
from shared.utils.validator import validate_email


class PaperAttrData(BaseDto):
    def __init__(self):
        self.title: str = ""
        self.keywords: str = ""
        self.abstract: str = ""
        self.publish_date: datetime = datetime.today()

    def is_valid(self) -> bool:
        return True


class PaperAuthorData(BaseDto):
    def __init__(self):
        self.email: str = ""
        self.name: str = ""
        self.order: int = 0

    def is_valid(self) -> bool:
        if not validate_email(self.email):
            return False
        return True


class PaperRefData(BaseDto):
    def __init__(self):
        self.text: str = ""
        self.link: str = ""

    def is_valid(self) -> bool:
        return not is_no_content(self.text)


class PaperPostDto(BaseDto):
    def __init__(self):
        self.attr: PaperAttrData = PaperAttrData()
        self.authors: List[PaperAuthorData] = [PaperAuthorData()]
        self.areas: List[int] = [0]
        self.refs: List[PaperRefData] = [PaperRefData()]

    def is_valid(self) -> bool:
        if not self.attr.is_valid():
            return False
        for author in self.authors:
            if not author.is_valid():
                print("invalid author")
                return False
        for area in self.areas:
            area = parse_value(area, int)
            if area is None:
                return False
        for ref in self.refs:
            if not ref.is_valid():
                return False
        return True


class PaperGetDto(PaperPostDto):
    def __init__(self):
        super().__init__()
        self.pid: int = 0
