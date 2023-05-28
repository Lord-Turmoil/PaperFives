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

from users.views.utils.stat import update_all_user_statistics, update_all_user_ranks


@shared_task
def update_user_statistics_task():
    update_all_user_statistics()
    update_all_user_ranks()
