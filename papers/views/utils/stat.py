# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/28/2023 12:56
# @Author  : Tony Skywalker
# @File    : stat.py
#
# Description:
#   Paper statistics update.
#
from papers.models import Paper, AreaStatistics


def _clear_area_statistics():
    areas = AreaStatistics.objects.all()
    for area in areas:
        area.cnt = 0
        area.save()


def _create_or_update_area_statistics(aid, publish_date):
    year = publish_date.year
    month = publish_date.month
    areas = AreaStatistics.objects.filter(aid=aid, year=year, month=month)
    if areas.exists():
        area = areas.first()
    else:
        area = AreaStatistics.create(aid, year, month)
    area.cnt += 1
    area.save()


def update_all_area_statistics():
    papers = Paper.objects.filter(status=Paper.Status.PASSED)

    _clear_area_statistics()
    for paper in papers:
        areas = paper.areas.all()
        for area in areas:
            _create_or_update_area_statistics(area.aid, paper.attr.publish_date)
