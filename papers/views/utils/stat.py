# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/28/2023 12:56
# @Author  : Tony Skywalker
# @File    : stat.py
#
# Description:
#   Paper statistics update.
#
from django.utils import timezone

from papers.models import Paper, AreaStatistics, PaperRank, PaperStatistics, Top20Paper, AreaRank, Area, Top20Area


######################################################################
# Area Statistics
#

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


######################################################################
# Paper Rank

def _evaluate_paper_rank(stat: PaperStatistics):
    rank = 0.0
    rank += stat.cites * 2.5
    rank += stat.downloads * 1.0
    rank += stat.favorites * 0.5
    rank += stat.clicks * 0.2
    return rank


def update_all_paper_ranks():
    PaperRank.objects.all().delete()

    for paper in Paper.objects.filter(status=Paper.Status.PASSED):
        val = _evaluate_paper_rank(paper.stat)
        rank = PaperRank.create(paper.pid, val).save()

    Top20Paper.objects.all().delete()
    ranks = PaperRank.objects.all().order_by('-rank')[:20]
    for rank in ranks:
        Top20Paper.create(rank.pid, rank.rank).save()


######################################################################
# Area Rank
#

def _get_date_diff(src_year, src_month, dst_year, dst_month):
    return dst_month - src_month + (dst_year - src_year) * 12


def _get_date_ratio(src_year, src_month, dst_year, dst_month):
    """
    The nearer, the better. Ratio > 1.0 if in 1 year.
    """
    diff = float(_get_date_diff(src_year, src_month, dst_year, dst_month)) + 1.0
    return float(12.0 / diff)


def _evaluate_area_rank(aid, current):
    rank = 0.0
    stats = AreaStatistics.objects.filter(aid=aid)
    for stat in stats:
        ratio = _get_date_ratio(stat.year, stat.month, current.year, current.month)
        rank += ratio * float(stat.cnt)
    return rank


def update_all_area_ranks():
    AreaRank.objects.all().delete()
    current = timezone.now()

    for area in Area.objects.all():
        val = _evaluate_area_rank(area.aid, current)
        AreaRank.create(area.aid, val).save()

    Top20Area.objects.all().delete()
    ranks = AreaRank.objects.all().order_by('-rank')[:20]
    for rank in ranks:
        Top20Area.create(rank.aid, rank.rank).save()


######################################################################
# Paper Statistics Auxiliary
#

def get_paper_rank_by_pid(pid):
    ranks = PaperRank.objects.filter(pid=pid)
    if ranks.exists():
        return ranks.first().rank
    return 0.0
