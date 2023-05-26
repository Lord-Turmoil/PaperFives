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
from papers.views.utils.serialize import get_paper_post_dto
from shared.utils.str_util import is_no_content


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


def is_paper_complete(paper) -> bool:
    if paper is None:
        return False
    if not get_paper_post_dto(paper):
        return False
    if is_no_content(paper.path):
        return False
    return True
