# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/28/2023 12:15
# @Author  : Tony Skywalker
# @File    : tasks.py
#
# Description:
#   Paper statistics update tasks.
#
from celery import shared_task

from papers.views.utils.stat import update_all_area_statistics


@shared_task
def update_area_statistics_task():
    update_all_area_statistics()
   