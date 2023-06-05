# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 6/4/2023 15:53
# @Author  : Tony Skywalker
# @File    : publish_stat.py
#
# Description:
#   For user publish statistics.
#
from typing import List

from shared.dtos.models.base import BaseDto
from shared.dtos.response.base import GoodResponseDto
from shared.utils.papers.areas import get_area_by_aid
from users.models import AreaPublishStatistics


# Publish Statistics Bar Chart

class UserPubStatBarItemData(BaseDto):
    def __init__(self):
        self.years: List[int] = [0]
        self.lead_cnt: List[int] = [0]
        self.co_cnt: List[int] = [0]

    def init(self, stats):
        self.years.clear()
        self.lead_cnt.clear()
        self.co_cnt.clear()
        for stat in stats:
            self.years.append(stat.year)
            self.lead_cnt.append(stat.lead_cnt)
            self.co_cnt.append(stat.co_cnt)
        return self


class UserPubStatBarDto(BaseDto):
    def __init__(self):
        super().__init__()
        self.uid: int = 0
        self.stats: UserPubStatBarItemData = UserPubStatBarItemData()

    def init(self, uid, stats):
        self.uid = uid
        self.stats.init(stats)
        return self


# Publish Statistics Pie Chart

class UserPubStatPieItemData(BaseDto):
    def __init__(self):
        self.name: str = ''
        self.value: int = 0

    def init(self, stat: AreaPublishStatistics):
        self.name = get_area_by_aid(stat.aid)
        if self.name is None:
            self.name = 'Else'
        else:
            self.name = self.name.name
        self.value = stat.cnt
        return self


class UserPubStatPieDto(GoodResponseDto):
    def __init__(self):
        super().__init__()
        self.uid: int = 0
        self.stats: List[UserPubStatPieItemData] = [UserPubStatPieItemData()]
        self.legend: List[str] = [""]

    def init(self, uid, stats):
        self.uid = uid
        self.stats.clear()
        self.legend.clear()
        for stat in stats:
            item = UserPubStatPieItemData().init(stat)
            self.stats.append(item)
            self.legend.append(item.name)

        return self
