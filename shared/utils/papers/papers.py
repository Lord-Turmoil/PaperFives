# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/24/2023 10:30
# @Author  : Tony Skywalker
# @File    : papers.py
#
from papers.models import Paper, PublishRecord


def get_paper_by_pid(pid):
    papers = Paper.objects.filter(pid=pid)
    if papers.exists():
        return papers.first()
    return None


def get_publish_record(uid, pid):
    records = PublishRecord.objects.filter(uid=uid, pid=pid)
    if records.exists():
       return records.first()
    return None
