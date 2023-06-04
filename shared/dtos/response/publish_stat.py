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
from users.models import PublishStatistics, AreaPublishStatistics


# Publish Statistics Bar Chart

class UserPubStatBarItemData(BaseDto):
    def __init__(self):
        self.year: int = 0
        self.lead_cnt: int = 0
        self.co_cnt: int = 0

    def init(self, stat: PublishStatistics):
        self.year = stat.year
        self.lead_cnt = stat.lead_cnt
        self.co_cnt = stat.co_cnt
        return self


class UserPubStatBarDto(GoodResponseDto):
    def __init__(self):
        super().__init__()
        self.uid: int = 0
        self.stats: List[UserPubStatBarItemData] = [UserPubStatBarItemData()]

    def init(self, uid, stats):
        self.uid = uid
        self.stats.clear()
        for stat in stats:
            self.stats.append(UserPubStatBarItemData().init(stat))
        return self


# Publish Statistics Pie Chart

class UserPubStatPieItemData(BaseDto):
    def __init__(self):
        self.aid: int = 0
        self.cnt: int = 0

    def init(self, stat: AreaPublishStatistics):
        self.aid = stat.aid
        self.cnt = stat.cnt
        return self


class UserPubStatPieDto(GoodResponseDto):
    def __init__(self):
        super().__init__()
        self.uid: int = 0
        self.stats: List[UserPubStatPieItemData] = [UserPubStatPieItemData()]

    def init(self, uid, stats):
        self.uid = uid
        self.stats.clear()
        for stat in stats:
            self.stats.append(UserPubStatPieItemData().init(stat))
        return self
