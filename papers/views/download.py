# Copyright (C) 2023 - 2023 Tony Skywalker. All Rights Reserved 
#
# @Time    : 5/25/2023 9:03
# @Author  : Tony Skywalker
# @File    : download.py
#
# Description:
#   Download actions.
#
from django.views.decorators.csrf import csrf_exempt

from papers.models import Paper
from papers.views.utils.serializer import get_paper_get_dto
from shared.dtos.response.base import GoodResponseDto
from shared.dtos.response.errors import RequestMethodErrorDto, BadRequestDto, PageNotFoundErrorDto
from shared.dtos.response.papers import NoSuchPaperErrorDto, PaperFileMissingErrorDto
from shared.dtos.response.users import NotLoggedInDto
from shared.response.basic import BadRequestResponse, GoodResponse
from shared.response.papers import PdfFileResponse
from shared.response.strict import HttpBadRequestResponse, HttpNotAuthorizedResponse, HttpPageNotFoundResponse
from shared.utils.papers.papers import get_paper_by_pid
from shared.utils.parameter import parse_param
from shared.utils.parser import parse_value
from shared.utils.str_util import is_no_content
from shared.utils.url_encoder import convert_to_url
from shared.utils.users.users import get_user_from_request
from users.models import User


@csrf_exempt
def download_info(request):
    """
    No login require.
    """
    if request.method != 'GET':
        return BadRequestResponse(RequestMethodErrorDto('GET', request.method))
    params = parse_param(request)
    pid = parse_value(params.get('pid'), int)
    mode = parse_value(params.get('click'), bool)
    if pid is None:
        return BadRequestResponse(BadRequestDto("Missing 'pid'"))

    paper: Paper = get_paper_by_pid(pid)
    if paper is None:
        return GoodResponse(NoSuchPaperErrorDto())

    if (mode is not None) and (mode is True):
        paper.stat.clicks += 1
        paper.stat.save()

    dto = get_paper_get_dto(paper)

    return GoodResponse(GoodResponseDto(data=dto))


@csrf_exempt
def download_paper(request):
    """
    Do not check in middleware, since another Http Status should be returned.
    """
    if request.method != 'GET':
        return HttpBadRequestResponse(RequestMethodErrorDto('GET', request.method))
    user: User = get_user_from_request(request)
    if user is None:
        return HttpNotAuthorizedResponse(NotLoggedInDto())

    params = parse_param(request)
    pid = parse_value(params.get('pid'), int)
    if pid is None:
        return HttpBadRequestResponse(BadRequestDto("Missing 'pid'"))

    paper: Paper = get_paper_by_pid(pid)
    if paper is None:
        return HttpPageNotFoundResponse(NoSuchPaperErrorDto())

    # it shouldn't be, but in case
    if is_no_content(paper.path):
        return HttpPageNotFoundResponse(PaperFileMissingErrorDto())

    try:
        file = open(paper.path, 'rb')
    except:
        return HttpPageNotFoundResponse(PageNotFoundErrorDto("This is not the paper you're looking for"))

    return PdfFileResponse(file, f"{convert_to_url(paper.attr.title)}.pdf")
