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

from papers.models import Paper
from papers.views.utils.query import advanced_search, ordinary_search
from papers.views.utils.serializer import get_paper_get_simple_dto
from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto, BadRequestDto
from shared.dtos.response.papers import SearchErrorDto
from shared.exceptions.json import JsonDeserializeException
from shared.exceptions.search import SearchErrorException
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
    """
    All trivial parameters will be popped out, make 'params' a cond list.
    """
    if request.method != 'POST':
        return BadRequestResponse(RequestMethodErrorDto('POST', request.method))

    params = parse_param(request)
    page_size = parse_value(params.get('ps'), int, 20)
    page_num = parse_value(params.get('p'), int, 1)
    if (page_size < 1) or (page_num < 1):
        return BadRequestResponse(BadRequestDto("Invalid value for pagination"))
    advanced = parse_value(params.pop('advanced', None), bool, None)
    if advanced is None:
        return BadRequestResponse(BadRequestDto("Must specify query mode"))

    cond = params.get('cond')
    if cond is None:
        return BadRequestResponse(BadRequestDto("What to look for?"))
    attr = params.get('attr')   # can be None

    if advanced:
        searcher = advanced_search
    else:
        searcher = ordinary_search

    try:
        papers = searcher({'attr': attr, 'cond': cond})
    except JsonDeserializeException as e:
        return BadRequestResponse(BadRequestDto(e))
    except SearchErrorException as e:
        return GoodResponse(SearchErrorDto(e))

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
