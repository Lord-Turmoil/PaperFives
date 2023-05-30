# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/28/2023 12:56
# @Author  : Tony Skywalker
# @File    : stat.py
#
# Description:
#   Paper statistics update.
#
from papers.models import Paper, AreaStatistics, PaperRank, PaperStatistics, Top20Paper


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
# Paper Statistics Auxiliary
#

def get_paper_rank_by_pid(pid):
    ranks = PaperRank.objects.filter(pid=pid)
    if ranks.exists():
        return ranks.first().rank
    return 0.0
