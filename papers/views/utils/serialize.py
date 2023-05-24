# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/24/2023 10:51
# @Author  : Tony Skywalker
# @File    : serialize.py
#
from papers.models import Paper, PaperUpdateRecord
from shared.dtos.models.papers import PaperPostDto, PaperGetDto


def get_paper_post_dto(paper: Paper):
    return PaperPostDto().init(paper)


def get_paper_get_dto(paper: Paper):
    records = PaperUpdateRecord.objects.filter(pid=paper.pid)
    if records.exists():
        return PaperGetDto().init(paper, records.first().update_time)
    else:
        return PaperGetDto().init(paper)
