# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/28/2023 15:02
# @Author  : Tony Skywalker
# @File    : hot.py
#
# Descriptions:
#   Hot area, paper, author...
#
from django.views.decorators.csrf import csrf_exempt

from papers.models import Top20Paper, Top20Area
from papers.views.utils.serializer import get_paper_get_dto
from shared.dtos.models.areas import AreaGetDto
from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto
from shared.response.basic import BadRequestResponse, GoodResponse
from shared.utils.papers.papers import get_area_by_aid, get_paper_by_pid


@csrf_exempt
def get_hot_areas(request):
    if request.method != 'GET':
        return BadRequestResponse(RequestMethodErrorDto('GET', request.method))

    data = {'areas': []}
    area_ranks = Top20Area.objects.all().order_by('-rank')
    for area_rank in area_ranks:
        area = get_area_by_aid(area_rank.aid)
        if area is None:
            continue
        data['areas'].append({'area': AreaGetDto().init(area), 'rank': area_rank.rank})

    return GoodResponse(GoodResponseDto(data=data))


@csrf_exempt
def get_hot_papers(request):
    if request.method != 'GET':
        return BadRequestResponse(RequestMethodErrorDto('GET', request.method))

    data = {'papers': []}
    paper_ranks = Top20Paper.objects.all().order_by('-rank')
    for paper_rank in paper_ranks:
        paper = get_paper_by_pid(paper_rank.pid)
        if paper is None:
            continue
        data['papers'].append({'paper': get_paper_get_dto(paper), 'rank': paper_rank.rank})

    return GoodResponse(GoodResponseDto(data=data))
