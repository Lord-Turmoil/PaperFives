# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/30/2023 0:02
# @Author  : Tony Skywalker
# @File    : papers.py
#
import datetime
from random import Random
from typing import List

from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from PaperFives.settings import CONFIG
from papers.models import PaperAttribute, Paper, PaperStatistics, Author, PublishRecord, PaperUpdateRecord, \
    FavoritePaper
from papers.views.utils.papers import delete_whole_paper, update_paper_update_record
from shared.dtos.models.base import BaseDto
from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto, BadRequestDto
from shared.dtos.response.papers import PaperExistsErrorDto
from shared.exceptions.json import JsonDeserializeException
from shared.response.basic import BadRequestResponse, GoodResponse
from shared.utils.json_util import deserialize
from shared.utils.papers.areas import get_area_by_name
from shared.utils.papers.papers import get_paper_by_title, get_paper_by_pid
from shared.utils.parameter import parse_param
from zeta.views.utils.users import import_user

"""
{
    "title": "From single to collective motion of social amoebae: a computational  study of interacting cells\n",
    "authors": [
        "Eduardo Moreno",
        "Robert Garrison",
        "Carsten Beta",
        "Sergio Alonso"
    ],
    "subject": "Cell Behavior (q-bio.CB)",
    "abstract": "The paper...",
    "date": "2021-12-29 ",
    "filename": "2112.14774.pdf",
    "keywords": [
        "cell",
        "cells",
        "collective",
        "mechanisms",
        "mechanism"
    ]
}
"""


class ImportPaperDto(BaseDto):
    def __init__(self):
        self.title: str = ""
        self.authors: List[str] = [""]
        self.subject: str = ""
        self.abstract: str = ""
        self.date: datetime.date = timezone.now().today()
        self.filename: str = ""
        self.keywords: List[str] = [""]


def _create_paper_attribute(data: ImportPaperDto):
    attr = PaperAttribute.create(data.title, ', '.join(data.keywords), data.abstract, data.date)
    attr.save()
    return attr


def _create_paper_statistics(data: ImportPaperDto):
    engine = Random()

    cites = engine.randint(0, 100)
    downloads = engine.randint(0, 60)
    favorites = engine.randint(0, 50)
    _l = max(cites, downloads, favorites)
    clicks = engine.randint(_l, _l * 2 + 10)

    stat = PaperStatistics.create(cites, downloads, favorites, clicks)
    stat.save()

    return stat


def _create_paper(data: ImportPaperDto):
    paper_path = f"{CONFIG['PAPER_PATH']}{data.filename}"

    # Attribute and Statistics
    attr = _create_paper_attribute(data)
    stat = _create_paper_statistics(data)
    paper = Paper.create(paper_path, attr, stat)
    paper.status = Paper.Status.PASSED
    paper.save()

    # Link areas
    paper.areas.clear()
    area = get_area_by_name(data.subject)
    if area is not None:
        paper.areas.add(area)
    paper.save()

    # Create Authors & Users
    i = 0
    for author in data.authors:
        # Create or Get Users
        user = import_user(author)
        user.stat.publish_cnt += 1
        user.stat.save()

        # Create Author
        Author.create(paper, user.email, user.username, i).save()

        # Create Publish Record
        PublishRecord.create(_uid=user.uid, _pid=paper.pid, _lead=(i == 0)).save()

        i += 1

    # Create paper update record
    update_paper_update_record(paper)

    return paper


def _link_areas(data: ImportPaperDto):
    area = get_area_by_name(data.subject)
    if area is None:
        return


@csrf_exempt
def import_paper(request):
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))

    params = parse_param(request)
    try:
        data: ImportPaperDto = deserialize(params, ImportPaperDto)
    except JsonDeserializeException as e:
        return BadRequestResponse(BadRequestDto(e))

    paper = get_paper_by_title(data.title)
    if paper is not None:
        return GoodResponse(PaperExistsErrorDto(data.title))

    _create_paper(data)

    return GoodResponse(GoodResponseDto(f"Paper '{data.title}' imported"))


def _delete_whole_paper(paper):
    paper.attr.delete()
    paper.stat.delete()
    paper.authors.all().delete()
    paper.references.all().delete()
    paper.areas.clear()

    PublishRecord.objects.filter(pid=paper.pid).delete()
    PaperUpdateRecord.objects.filter(pid=paper.pid).delete()
    FavoritePaper.objects.filter(pid=paper.pid).delete()

    paper.delete()


@csrf_exempt
def clear_papers(request):
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))

    pid_list = [paper.pid for paper in Paper.objects.all()]
    for pid in pid_list:
        paper = get_paper_by_pid(pid)
        if paper:
            _delete_whole_paper(paper)

    return GoodResponse(GoodResponseDto(f"All papers deleted!"))
