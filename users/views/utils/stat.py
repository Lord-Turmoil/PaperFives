# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/27/2023 23:42
# @Author  : Tony Skywalker
# @File    : stat.py
#
from papers.models import PublishRecord, Paper
from papers.views.utils.stat import get_paper_rank_by_pid
from shared.utils.papers.papers import get_paper_by_pid
from users.models import User, PublishStatistics, UserRank


######################################################################
# User Statistics
#

def _clear_publish_statistics(uid):
    stats = PublishStatistics.objects.filter(uid=uid)
    for stat in stats:
        stat.lead_cnt = 0
        stat.co_cnt = 0
        stat.save()


def _get_or_create_publish_statistics(uid, year):
    stats = PublishStatistics.objects.filter(uid=uid, year=year)
    if stats.exists():
        return stats.first()
    else:
        stat = PublishStatistics.create(uid, year)
        stat.save()
        return stat


def _create_or_update_publish_statistics(uid, pid, lead):
    paper: Paper = get_paper_by_pid(pid)
    if (paper is None) or (paper.status != Paper.Status.PASSED):
        return

    year = paper.attr.publish_date.year
    stat: PublishStatistics = _get_or_create_publish_statistics(uid, year)
    if lead:
        stat.lead_cnt += 1
    else:
        stat.co_cnt += 1
    stat.save()


def update_all_user_statistics():
    users = User.objects.all()

    for user in users:
        _clear_publish_statistics(user.uid)

        records = PublishRecord.objects.filter(uid=user.uid)
        for record in records:
            _create_or_update_publish_statistics(user.uid, record.pid, record.lead)


######################################################################
# User Ranks
#

def _evaluate_user_rank(user: User):
    if not user.scholar:
        return 0.0

    rank = 0.0
    records = PublishRecord.objects.filter(uid=user.uid)
    for record in records:
        r = get_paper_rank_by_pid(record.pid)
        rank += (0.8 if record.lead else 0.2) * r

    return rank


def update_all_user_ranks():
    """
    Depends on 'update_all_user_statistics'
    """
    UserRank.objects.all().delete()

    for user in User.objects.filter(scholar=True):
        val = _evaluate_user_rank(user)
        rank = UserRank.create(user.uid, val)
        rank.save()


######################################################################
# User Statistics Auxiliary
#

def get_user_rank_by_pid(pid):
    ranks = UserRank.objects.filter(pid=pid)
    if ranks.exists():
        return ranks.first().rank
    return 0.0
