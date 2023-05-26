# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/26/2023 16:23
# @Author  : Tony Skywalker
# @File    : areas.py
#
from typing import List

from papers.models import Area, Paper
from shared.dtos.models.base import BaseDto


class AreaPostDto(BaseDto):
    def __init__(self):
        self.primary: int = 0
        self.secondary: int = 0
        self.name: str = ""


class AreaPostListDto(BaseDto):
    def __init__(self):
        self.areas: List[AreaPostDto] = [AreaPostDto()]


class AreaGetDto(AreaPostDto):
    def __init__(self):
        super().__init__()
        self.id: int = 0

    def init(self, area: Area):
        self.id = area.aid
        self.primary = area.primary
        self.secondary = area.secondary
        self.name = area.name
        return self


class AreaGetListDto(BaseDto):
    def __init__(self):
        self.areas: List[AreaGetDto] = [AreaGetDto()]

    def init(self, paper: Paper):
        self.areas = [AreaGetDto().init(area) for area in paper.areas.all()]
        return self
