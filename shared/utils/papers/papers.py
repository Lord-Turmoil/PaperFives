# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/24/2023 10:30
# @Author  : Tony Skywalker
# @File    : papers.py
#
from papers.models import Paper, PublishRecord, Area, AreaStatistics, FavoritePaper


def get_paper_by_pid(pid):
    papers = Paper.objects.filter(pid=pid)
    if papers.exists():
        return papers.first()
    return None


def get_paper_by_title(title: str):
    papers = Paper.objects.filter(attr__title=title)
    if papers.exists():
        return papers.first()
    return None


def get_publish_record(uid, pid):
    records = PublishRecord.objects.filter(uid=uid, pid=pid)
    if records.exists():
        return records.first()
    return None


def get_area_by_aid(aid):
    areas = Area.objects.filter(aid=aid)
    if areas.exists():
        return areas.first()
    return None


def get_area_cnt_by_aid(aid):
    stats = AreaStatistics.objects.filter(aid=aid)
    if stats.exists():
        return stats.first().cnt
    else:
        return 0


def is_favorite_paper_by_uid(uid, pid):
    papers = FavoritePaper.objects.filter(uid=uid, pid=pid)
    if papers.exists():
        return True
    return False
