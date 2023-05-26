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

from papers.models import Paper, PaperAttribute, Author, Reference, PaperStatistics
from shared.dtos.models.base import BaseDto
from shared.utils.parser import parse_value
from shared.utils.str_util import is_no_content
from shared.utils.validator import validate_email


class BasePaperDto(BaseDto):
    def is_valid(self) -> bool:
        return True

    def strip_content(self):
        for v in self.__dict__.values():
            if isinstance(v, str):
                v = v.strip()

    def is_complete(self) -> bool:
        for v in self.__dict__.values():
            if isinstance(v, str):
                if is_no_content(v):
                    return False
        return True


class PaperAttrData(BasePaperDto):
    def __init__(self):
        self.title: str = ""
        self.keywords: List[str] = [""]
        self.abstract: str = ""
        self.publish_date: datetime = datetime.today()

    def init(self, attr: PaperAttribute):
        self.title = attr.title
        self.keywords = attr.keywords.split(', ')
        self.abstract = attr.abstract
        self.publish_date = attr.publish_date
        return self


class PaperAuthorData(BasePaperDto):
    def __init__(self):
        self.email: str = ""
        self.name: str = ""
        self.order: int = 0

    def init(self, author: Author):
        self.email = author.email
        self.name = author.name
        self.order = author.order
        return self

    def is_complete(self) -> bool:
        if not validate_email(self.email):
            return False
        if is_no_content(self.name):
            return False
        return True


class PaperRefData(BasePaperDto):
    def __init__(self):
        self.text: str = ""
        self.link: str = ""

    def init(self, ref: Reference):
        self.text = ref.ref
        self.link = ref.link
        return self

    def is_complete(self) -> bool:
        self.text = self.text.strip()
        self.link = self.link.strip()
        return not is_no_content(self.text)


class PaperPostDto(BasePaperDto):
    def __init__(self):
        self.pid: int = 0
        self.attr: PaperAttrData = PaperAttrData()
        self.authors: List[PaperAuthorData] = [PaperAuthorData()]
        self.areas: List[int] = [0]
        self.refs: List[PaperRefData] = [PaperRefData()]

    def init(self, paper: Paper):
        self.pid = paper.pid
        self.attr = PaperAttrData().init(paper.attr)
        self.authors = [PaperAuthorData().init(author) for author in paper.authors.all()]
        self.areas = [area.aid for area in paper.areas.all()]
        self.refs = [PaperRefData().init(ref) for ref in paper.references.all()]
        return self

    def strip_content(self):
        self.attr.strip_content()
        for author in self.authors:
            author.strip_content()
        for ref in self.refs:
            ref.strip_content()

    def is_complete(self) -> bool:
        if not self.attr.is_complete():
            return False
        for author in self.authors:
            if not author.is_complete():
                return False
        if len(self.areas) == 0:
            return False
        for area in self.areas:
            area = parse_value(area, int)
            if area is None:
                return False
        for ref in self.refs:
            if not ref.is_complete():
                return False


class PaperStatData(BasePaperDto):
    def __init__(self):
        self.cites: int = 0
        self.downloads: int = 0
        self.favorites: int = 0
        self.clicks: int = 0

    def init(self, stat: PaperStatistics):
        self.cites = stat.cites
        self.downloads = stat.downloads
        self.favorites = stat.favorites
        self.clicks = stat.clicks
        return self


class PaperGetDto(PaperPostDto):
    def __init__(self):
        super().__init__()
        self.areas: List[str] = [""]  # override parent areas
        self.status: int = 0
        self.stat: PaperStatData = PaperStatData()
        self.update: str = ""  # last update time

    def init(self, paper, update=""):
        super().init(paper)
        # still override parent areas, but take one extra step
        self.areas = [area.name for area in paper.areas.all()]

        self.status = paper.status
        self.stat = PaperStatData().init(paper.stat)
        self.update = update

        return self
