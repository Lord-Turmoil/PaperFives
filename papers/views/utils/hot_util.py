# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/28/2023 15:09
# @Author  : Tony Skywalker
# @File    : hot_util.py
#
# Description:
#   Utility functions for hot related functions.
#
from papers.models import AreaStatistics


def get_hot_areas_aux(year, month):
    areas = AreaStatistics.objects.filter(year=year, month=month).order_by('-cnt')
    return areas
