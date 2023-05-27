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
from papers.models import PaperUpdateRecord, Paper, PublishRecord, FavoritePaper
from papers.views.utils.serialize import get_paper_post_dto
from shared.utils.str_util import is_no_content


def delete_paper_file(paper) -> bool:
    try:
        os.remove(paper.path)  # remove old paper
    except Exception as e:
        print(e)
        return False

    return True


def delete_whole_paper(paper: Paper):
    paper.attr.delete()
    paper.stat.delete()
    paper.authors.all().delete()
    paper.references.all().delete()
    paper.areas.clear()

    if not is_no_content(paper.path):
        delete_paper_file(paper)

    PublishRecord.objects.filter(pid=paper.pid).delete()
    PaperUpdateRecord.objects.filter(pid=paper.pid).delete()
    FavoritePaper.objects.filter(pid=paper.pid).delete()

    paper.delete()


def save_paper_file(paper: Paper, file) -> bool:
    path = f"{CONFIG['PAPER_PATH']}{paper.pid}.pdf"
    try:
        with open(path, "wb") as f:
            for chunk in file.chunks():
                f.write(chunk)
    except Exception as e:
        print(e)
        return False

    if paper.path != path:
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
    if not get_paper_post_dto(paper).is_complete():
        return False
    if is_no_content(paper.path):
        return False
    return True
