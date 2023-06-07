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

from datetime import datetime, date
from typing import List

from PaperFives.settings import CONFIG
from papers.models import Paper, PaperAttribute, Author, Reference, PaperStatistics
from shared.dtos.models.areas import AreaGetDto
from shared.dtos.models.base import BaseDto
from shared.utils.parser import parse_value
from shared.utils.str_util import is_no_content
from shared.utils.users.users import get_user_by_email
from shared.utils.validator import validate_email
from users.models import User


class AbstractPaperDto(BaseDto):
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


######################################################################
# Paper Data
#
class PaperAttrData(AbstractPaperDto):
    def __init__(self):
        super().__init__()
        self.title: str = ""
        self.keywords: List[str] = [""]
        self.abstract: str = ""
        self.publish_date: date = date.today()

    def init(self, attr: PaperAttribute):
        self.title = attr.title
        self.keywords = attr.keywords.split(', ')
        self.abstract = attr.abstract
        self.publish_date = attr.publish_date
        return self


class BasePaperAuthorData(AbstractPaperDto):
    def __init__(self):
        super().__init__()
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


class PaperAuthorPostData(BasePaperAuthorData):
    def __init__(self):
        super().__init__()

    def init(self, author: Author):
        super().init(author)
        return self

    def is_complete(self) -> bool:
        if not validate_email(self.email):
            return False
        if is_no_content(self.name):
            return False
        return True


class PaperAuthorGetData(BasePaperAuthorData):
    def __init__(self):
        super().__init__()
        self.uid: int = 0

    def init(self, author: Author):
        super().init(author)
        user: User = get_user_by_email(self.email)
        self.uid = user.uid if user is not None else 0
        return self

    def is_complete(self) -> bool:
        if not validate_email(self.email):
            return False
        if is_no_content(self.name):
            return False
        return True


class PaperRefData(AbstractPaperDto):
    def __init__(self):
        super().__init__()
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


######################################################################
# Paper Detailed Dto
#
class BasePaperDto(AbstractPaperDto):
    def __init__(self):
        super().__init__()
        self.pid: int = 0
        self.attr: PaperAttrData = PaperAttrData()
        self.refs: List[PaperRefData] = [PaperRefData()]

    def init(self, paper: Paper):
        self.pid = paper.pid
        self.attr = PaperAttrData().init(paper.attr)
        self.refs = [PaperRefData().init(ref) for ref in paper.references.all()]
        return self


class PaperPostDto(BasePaperDto):
    def __init__(self):
        super().__init__()
        self.authors: List[PaperAuthorPostData] = [PaperAuthorPostData()]
        self.areas: List[int] = [0]

    def init(self, paper: Paper):
        super().init(paper)
        self.areas = [area.aid for area in paper.areas.all()]
        self.authors = [PaperAuthorPostData().init(author) for author in paper.authors.all()]
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
        return True


class PaperStatData(AbstractPaperDto):
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


class BasePaperGetDto(BasePaperDto):
    def __init__(self):
        super().__init__()
        self.areas: List[AreaGetDto] = [AreaGetDto()]
        self.stat: PaperStatData = PaperStatData()
        self.status: int = 0
        self.update: str = ""  # last update time

    def init(self, paper, update=""):
        super().init(paper)
        self.areas = [AreaGetDto().init(area) for area in paper.areas.all()]
        self.stat = PaperStatData().init(paper.stat)
        self.status = paper.status
        self.update = update
        return self


class PaperGetDto(BasePaperGetDto):
    def __init__(self):
        super().__init__()
        self.authors: List[PaperAuthorGetData] = [PaperAuthorGetData()]

    def init(self, paper, update=""):
        super().init(paper)
        self.authors = [PaperAuthorGetData().init(author) for author in paper.authors.all()]
        return self


######################################################################
# Paper Simple Dto
#
class PaperAttrSimpleData(AbstractPaperDto):
    def __init__(self):
        super().__init__()
        self.title: str = ""
        self.keywords: List[str] = [""]
        self.abstract: str = ""  # cut
        self.publish_date: datetime = datetime.today()

    def init(self, attr: PaperAttribute):
        self.title = attr.title
        self.keywords = attr.keywords.split(', ')
        self.abstract = attr.abstract[:255]
        while (len(self.abstract) > 0) and (self.abstract[-1] != ' '):
            self.abstract = self.abstract.rstrip(self.abstract[-1])
        self.abstract += "..."
        self.publish_date = attr.publish_date
        return self


class PaperGetSimpleDto(AbstractPaperDto):
    def __init__(self):
        super().__init__()
        self.pid: int = 0
        self.attr: PaperAttrSimpleData = PaperAttrSimpleData()
        self.authors: List[PaperAuthorGetData] = [PaperAuthorGetData()]
        self.stat: PaperStatData = PaperStatData()
        self.areas: List[AreaGetDto] = [AreaGetDto()]
        self.update: str = ""

    def init(self, paper, update=""):
        self.pid = paper.pid
        self.attr = PaperAttrSimpleData().init(paper.attr)
        self.authors = [PaperAuthorGetData().init(author) for author in paper.authors.all()]
        self.stat = PaperStatData().init(paper.stat)
        self.areas = [AreaGetDto().init(area) for area in paper.areas.all()]
        self.update = update
        return self


class PaperGetUserDto(PaperGetSimpleDto):
    def __init__(self):
        super().__init__()
        self.status: int = 0
        self.lead: bool = False

    def init(self, paper, update="", lead=False):
        super().init(paper, update)
        self.status = paper.status
        self.lead = lead
        return self


######################################################################
# Paper Detail Info
#

class PaperAuthorDetailGetData(BasePaperAuthorData):
    def __init__(self):
        super().__init__()
        self.uid: int = 0
        self.avatar: str = ""

    def init(self, author: Author):
        super().init(author)
        user: User = get_user_by_email(self.email)
        self.uid = user.uid if user is not None else 0
        self.avatar = user.avatar if user is not None else CONFIG['DEFAULT_AVATAR']
        return self


class PaperGetDetailDto(BasePaperGetDto):
    def __init__(self):
        super().__init__()
        self.authors: List[PaperAuthorDetailGetData] = [PaperAuthorDetailGetData()]

    def init(self, paper, update=""):
        super().init(paper, update)
        self.authors = [PaperAuthorDetailGetData().init(author) for author in paper.authors.all()]
        return self
