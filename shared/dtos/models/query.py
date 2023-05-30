# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/28/2023 22:16
# @Author  : Tony Skywalker
# @File    : query.py
#
from typing import List

from shared.dtos.models.base import BaseDto


class OrdinaryCond(BaseDto):
    def __init__(self):
        self.field: str = ""
        self.key: str = ""


class OrdinaryCondList(BaseDto):
    def __init__(self):
        self.cond: OrdinaryCond = OrdinaryCond()


class AdvancedCond(OrdinaryCond):
    def __init__(self):
        super().__init__()
        self.mode: str = ""


class AdvancedCondList(BaseDto):
    def __init__(self):
        self.cond: List[AdvancedCond] = [AdvancedCond()]
