# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/28/2023 22:16
# @Author  : Tony Skywalker
# @File    : query.py
#
from datetime import datetime
from typing import List

from django.utils import timezone

from shared.dtos.models.base import BaseDto


class CondAttr(BaseDto):
    def __init__(self):
        """
        time_from/to must strictly be YYYY-MM-DD format
        """
        super().__init__()
        self.order: str = ""
        self.time_from: datetime = timezone.now()
        self.time_to: datetime = timezone.now()


class OrdinaryCond(BaseDto):
    def __init__(self):
        self.field: str = ""
        self.key: str = ""


class OrdinaryCondList(BaseDto):
    def __init__(self):
        super().__init__()
        self.cond: OrdinaryCond = OrdinaryCond()


class AdvancedCond(OrdinaryCond):
    def __init__(self):
        super().__init__()
        self.mode: str = ""


class AdvancedCondList(BaseDto):
    def __init__(self):
        super().__init__()
        self.cond: List[AdvancedCond] = [AdvancedCond()]
