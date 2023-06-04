# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/27/2023 23:36
# @Author  : Tony Skywalker
# @File    : tasks.py
#
# Description:
#   For user update tasks.
#
from celery import shared_task

from users.models import User, PublishStatistics
from users.views.register import _erase_user
from users.views.utils.stat import update_all_user_statistics, update_all_user_ranks, update_all_user_area_statistics


@shared_task
def update_user_statistics_task():
    update_all_user_statistics()
    update_all_user_area_statistics()
    update_all_user_ranks()


@shared_task
def remove_stupid_users_task():
    stupid_list = []
    for user in User.objects.all():
        records = PublishStatistics.objects.filter(uid=user.uid)
        lead = 0
        for record in records:
            lead += record.lead_cnt
        if lead == 0:  # no lead position
            stupid_list.append(user)

    for stupid in stupid_list:
        _erase_user(stupid.uid)
        stupid.attr.delete()
        stupid.stat.delete()
        stupid.delete()
