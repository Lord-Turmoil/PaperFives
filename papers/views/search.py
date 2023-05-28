# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/27/2023 21:25
# @Author  : Tony Skywalker
# @File    : search.py
#
# Description:
#   Search papers.
#
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from haystack.query import SearchQuerySet

from papers.models import Paper
from papers.views.utils.serializer import get_paper_get_simple_dto
from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto, BadRequestDto
from shared.response.basic import BadRequestResponse, GoodResponse
from shared.utils.papers.papers import get_paper_by_pid
from shared.utils.parameter import parse_param
from shared.utils.parser import parse_value


@csrf_exempt
def temp_get_pid_list(request):
    if request.method != 'GET':
        return BadRequestResponse(RequestMethodErrorDto('GET', request.method))

    papers = Paper.objects.all()
    paper_list = []
    for paper in papers:
        paper_list.append(paper.pid)

    return GoodResponse(GoodResponseDto(data=paper_list))


@csrf_exempt
def query_paper(request):
    if request.method != 'GET':
        return BadRequestResponse(RequestMethodErrorDto('GET', request.method))

    params = parse_param(request)
    page_size = parse_value(params.get('ps', 20), int)
    page_num = parse_value(params.get('p', 1), int)
    if (page_size is None) or (page_num is None) or (page_size < 1) or (page_num < 1):
        return BadRequestResponse(BadRequestDto("Invalid value for pagination"))

    papers = SearchQuerySet().models(Paper).all()

    paginator = Paginator(papers, page_size)
    page = paginator.get_page(page_num)

    # construct result
    data = {
        'ps': page_size,
        'p': page.number,
        'total': papers.count(),
        'next': paginator.num_pages > page.number,
        'papers': []
    }

    # the result in search is not complete
    for paper in page.object_list:
        db_paper = get_paper_by_pid(paper.pid)
        if db_paper is not None:
            data['papers'].append(get_paper_get_simple_dto(db_paper))

    return GoodResponse(GoodResponseDto(data=data))
