# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/24/2023 13:23
# @Author  : Tony Skywalker
# @File    : papers.py
#
# Description:
#   Operations on papers.
#
import os

from django.utils import timezone

from PaperFives.settings import CONFIG
from papers.models import PaperUpdateRecord


def remove_paper_file(paper) -> bool:
    try:
        os.remove(paper.path)  # remove old paper
    except Exception as e:
        print(e)
        return False
    paper.path = ""
    paper.save()
    return True


def save_paper_file(paper, file) -> bool:
    path = f"{CONFIG['PAPER_PATH']}{paper.pid}.pdf"
    try:
        f = open(path, "wb")
        for chunk in file.chunks():
            f.write(chunk)
        f.close()
    except Exception as e:
        print(e)
        return False
    paper.path = path
    paper.save()
    return True


def update_paper_update_record(paper):
    records = PaperUpdateRecord.objects.filter(pid=paper.pid)
    if records.exists():
        record: PaperUpdateRecord = records.first()
        record.update_time = timezone.now()
    else:
        record = PaperUpdateRecord.create(paper.pid)
    record.save()
